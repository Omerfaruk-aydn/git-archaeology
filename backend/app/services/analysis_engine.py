from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging
from collections import defaultdict
import asyncio

from sqlalchemy.orm import Session

from app.models.repository import Commit, FileChange, Analysis, Repository
from app.services.git_service import GitService, GitCommitInfo
from app.services.llm_service import LLMService
from app.schemas.repository import AnalysisCreate

logger = logging.getLogger(__name__)


class AnalysisEngine:
    def __init__(self, db: Session, git_service: GitService, llm_service: LLMService):
        self.db = db
        self.git = git_service
        self.llm = llm_service

    async def run_full_analysis(
        self,
        repo: Repository,
        config: AnalysisCreate,
    ) -> Analysis:
        analysis = Analysis(
            repository_id=repo.id,
            status="running",
            config=config.model_dump(),
            started_at=datetime.utcnow(),
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        try:
            commits = self.git.get_commits(
                branch=config.branch or repo.default_branch,
                max_count=config.max_commits,
                start_date=config.start_date,
                end_date=config.end_date,
            )

            analysis.total_commits = len(commits)
            self.db.commit()

            for i in range(0, len(commits), config.batch_size):
                batch = commits[i:i + config.batch_size]
                await self._process_commit_batch(batch, analysis, config)
                analysis.processed_commits = i + len(batch)
                analysis.progress = (i + len(batch)) / len(commits) * 100
                self.db.commit()

            summary = await self._generate_summary(analysis, repo, config)
            analysis.result = summary
            analysis.status = "completed"
            analysis.completed_at = datetime.utcnow()
            analysis.progress = 100.0
            self.db.commit()

        except Exception as e:
            logger.error(f"Analiz hatası: {e}")
            analysis.status = "failed"
            analysis.error_message = str(e)
            self.db.commit()

        return analysis

    async def _process_commit_batch(
        self,
        commits: List[GitCommitInfo],
        analysis: Analysis,
        config: AnalysisCreate,
    ):
        for commit_info in commits:
            existing = self.db.query(Commit).filter(
                Commit.sha == commit_info.sha,
                Commit.analyzed == True,
            ).first()

            if existing:
                continue

            commit = self.db.query(Commit).filter(Commit.sha == commit_info.sha).first()
            if not commit:
                commit = Commit(
                    repository_id=analysis.repository_id,
                    sha=commit_info.sha,
                    message=commit_info.message,
                    author_name=commit_info.author_name,
                    author_email=commit_info.author_email,
                    author_date=commit_info.author_date,
                    committer_name=commit_info.committer_name,
                    committer_email=commit_info.committer_email,
                    committer_date=commit_info.committer_date,
                    parents=commit_info.parents,
                )
                self.db.add(commit)

            stats = self.git.get_commit_stats(commit_info.sha)
            commit.additions = stats.get("insertions", 0)
            commit.deletions = stats.get("deletions", 0)
            commit.files_changed = stats.get("files_changed", 0)

            if config.include_diffs:
                file_changes = self.git.get_file_changes(commit_info.sha, include_diff=True)
                for fc in file_changes:
                    file_change = FileChange(
                        commit_id=commit.id,
                        file_path=fc.file_path,
                        old_path=fc.old_path,
                        change_type=fc.change_type,
                        additions=fc.additions,
                        deletions=fc.deletions,
                        diff=fc.diff,
                        old_content=fc.old_content,
                        new_content=fc.new_content,
                    )
                    self.db.add(file_change)

            if config.focus_areas:
                analysis_prompt = self._build_commit_analysis_prompt(commit, file_changes if config.include_diffs else [])
                llm_result = await self.llm.analyze_commit(
                    commit_message=commit.message,
                    file_changes=[fc.model_dump() for fc in (file_changes if config.include_diffs else [])],
                    focus_areas=config.focus_areas,
                )
                commit.analysis_result = llm_result
                commit.analyzed = True

            self.db.add(commit)
            self.db.commit()

    def _build_commit_analysis_prompt(self, commit: Commit, file_changes: list) -> str:
        prompt = f"""Bu Git commit'unu analiz et:

Commit: {commit.sha[:8]}
Mesaj: {commit.message}
Yazar: {commit.author_name}
Tarih: {commit.author_date.isoformat()}
Değişiklikler: +{commit.additions} -{commit.deletions} ({commit.files_changed} dosya)

Değişen dosyalar:
"""

        for fc in file_changes[:20]:
            prompt += f"\n- {fc.file_path} ({fc.change_type}): +{fc.additions} -{fc.deletions}"
            if fc.diff:
                diff_preview = fc.diff[:1000]
                prompt += f"\n  Diff: {diff_preview}\n"

        prompt += """
\nBu commit'u şu açılardan analiz et:
1. Güvenlik (security) - Güvenlik açığı veya zafiyet var mı?
2. Performans - Performans etkileyen değişiklikler var mı?
3. Mimari - Mimari yapıyı etkileyen değişiklikler var mı?
4. Bağımlılık - Yeni bağımlılık veya bağımlılık güncellemesi var mı?
5. Koddokuşması - Kod kalitesini etkileyen değişiklikler var mı?

Yanıtını JSON formatında ver:
{
  "summary": "Kısa özet",
  "category": "security|performance|architecture|dependency|refactor|feature|bugfix|other",
  "importance": "high|medium|low",
  "tags": ["tag1", "tag2"],
  "insights": ["insight1", "insight2"],
  "related_files": ["file1", "file2"],
  "recommendations": ["rec1", "rec2"]
}"""
        return prompt

    async def _generate_summary(
        self,
        analysis: Analysis,
        repo: Repository,
        config: AnalysisCreate,
    ) -> Dict[str, Any]:
        commits = self.db.query(Commit).filter(
            Commit.repository_id == repo.id,
            Commit.analyzed == True,
        ).all()

        total_additions = sum(c.additions for c in commits)
        total_deletions = sum(c.deletions for c in commits)
        unique_authors = list(set(c.author_name for c in commits))

        file_changes = self.db.query(FileChange).join(Commit).filter(
            Commit.repository_id == repo.id,
        ).all()

        file_frequency = defaultdict(int)
        for fc in file_changes:
            file_frequency[fc.file_path] += 1

        top_files = sorted(file_frequency.items(), key=lambda x: x[1], reverse=True)[:20]

        categories = defaultdict(int)
        for commit in commits:
            if commit.analysis_result and "category" in commit.analysis_result:
                categories[commit.analysis_result["category"]] += 1

        date_buckets = defaultdict(int)
        for commit in commits:
            date_key = commit.author_date.strftime("%Y-%m")
            date_buckets[date_key] += 1

        summary = {
            "total_commits": len(commits),
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "unique_authors": len(unique_authors),
            "authors": unique_authors,
            "date_range": {
                "start": min(c.author_date for c in commits).isoformat() if commits else None,
                "end": max(c.author_date for c in commits).isoformat() if commits else None,
            },
            "top_files": [{"path": f, "changes": c} for f, c in top_files],
            "category_distribution": dict(categories),
            "activity_timeline": dict(date_buckets),
        }

        summary_prompt = f"""Aşağıdaki Git deposu analiz sonuçlarını özetle:

Depo: {repo.name}
Toplam Commit: {len(commits)}
Yazar Sayısı: {len(unique_authors)}
Toplam Değişiklik: +{total_additions} -{total_deletions}

En çok değişen dosyalar:
{chr(10).join([f'- {f}: {c} değişiklik' for f, c in top_files[:10]])}

Kategori dağılımı:
{chr(10).join([f'- {k}: {v} commit' for k, v in categories.items()])}

Bu analiz için:
1. Genel bir özet yaz
2. Önemli trendleri belirle
3. Potansiyel riskleri tanımla
4. Öneriler sun

Yanıtını JSON formatında ver:
{
  "overall_summary": "...",
  "key_trends": ["trend1", "trend2"],
  "potential_risks": ["risk1", "risk2"],
  "recommendations": ["rec1", "rec2"],
  "highlights": ["highlight1", "highlight2"]
}"""

        llm_summary = await self.llm.generate_summary(summary_prompt)

        summary["llm_summary"] = llm_summary
        return summary
