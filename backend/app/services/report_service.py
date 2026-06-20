import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import markdown
import logging

from sqlalchemy.orm import Session

from app.models.repository import Repository, Analysis, Commit, FileChange
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm = llm_service

    async def generate_report(
        self,
        repository_id: str,
        report_type: str,
        branch: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        file_paths: Optional[list[str]] = None,
        format: str = "markdown",
    ) -> Dict[str, Any]:
        repo = self.db.query(Repository).filter(Repository.id == repository_id).first()
        if not repo:
            raise ValueError("Depo bulunamadı")

        query = self.db.query(Commit).filter(Commit.repository_id == repository_id)

        if start_date:
            query = query.filter(Commit.author_date >= start_date)
        if end_date:
            query = query.filter(Commit.author_date <= end_date)

        commits = query.order_by(Commit.author_date.desc()).all()

        file_changes = []
        if file_paths:
            file_changes = self.db.query(FileChange).join(Commit).filter(
                Commit.repository_id == repository_id,
                FileChange.file_path.in_(file_paths),
            ).all()

        analysis_data = {
            "repository": {
                "name": repo.name,
                "url": repo.url,
                "default_branch": repo.default_branch,
            },
            "commits": [
                {
                    "sha": c.sha,
                    "message": c.message,
                    "author": c.author_name,
                    "date": c.author_date.isoformat(),
                    "additions": c.additions,
                    "deletions": c.deletions,
                    "analysis": c.analysis_result,
                }
                for c in commits[:500]
            ],
            "file_changes": [
                {
                    "path": fc.file_path,
                    "change_type": fc.change_type,
                    "additions": fc.additions,
                    "deletions": fc.deletions,
                    "analysis": fc.analysis,
                }
                for fc in file_changes[:200]
            ],
            "statistics": {
                "total_commits": len(commits),
                "total_additions": sum(c.additions for c in commits),
                "total_deletions": sum(c.deletions for c in commits),
                "unique_authors": len(set(c.author_name for c in commits)),
            },
        }

        report_content = await self.llm.generate_report(analysis_data, report_type)

        if format == "html":
            report_content = self._markdown_to_html(report_content)

        return {
            "content": report_content,
            "format": format,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "report_type": report_type,
                "commit_count": len(commits),
                "date_range": {
                    "start": commits[-1].author_date.isoformat() if commits else None,
                    "end": commits[0].author_date.isoformat() if commits else None,
                },
            },
        }

    async def generate_archeological_report(
        self,
        repository_id: str,
        file_path: str,
    ) -> str:
        repo = self.db.query(Repository).filter(Repository.id == repository_id).first()
        if not repo:
            raise ValueError("Depo bulunamadı")

        file_changes = self.db.query(FileChange).join(Commit).filter(
            Commit.repository_id == repository_id,
            FileChange.file_path == file_path,
        ).order_by(Commit.author_date).all()

        if not file_changes:
            return f"Bu dosya için değişiklik bulunamadı: {file_path}"

        context = f"Dosya: {file_path}\n"
        context += f"Toplam Değişiklik Sayısı: {len(file_changes)}\n"
        context += f"İlk Değişiklik: {file_changes[0].commit.author_date.isoformat()}\n"
        context += f"Son Değişiklik: {file_changes[-1].commit.author_date.isoformat()}\n\n"

        context += "Değişiklik Geçmişi:\n"
        for fc in file_changes:
            context += f"\n---\n"
            context += f"Commit: {fc.commit.sha[:8]}\n"
            context += f"Tarih: {fc.commit.author_date.isoformat()}\n"
            context += f"Yazar: {fc.commit.author_name}\n"
            context += f"Mesaj: {fc.commit.message}\n"
            context += f"Değişiklik Türü: {fc.change_type}\n"
            context += f"Eklenen: +{fc.additions}, Silinen: -{fc.deletions}\n"
            if fc.old_content:
                context += f"Eski Kod (ilk 500 karakter):\n```\n{fc.old_content[:500]}\n```\n"
            if fc.new_content:
                context += f"Yeni Kod (ilk 500 karakter):\n```\n{fc.new_content[:500]}\n```\n"

        prompt = f"""{context}

Bu dosyanın arkeolojik analizini oluştur. Raporda şunları belirt:

1. **Dosya Özeti**: Bu dosya ne işe yarar?
2. **Gelişim Tarihçesi**: Dosya nasıl evrildi?
3. **Kritik Değişiklikler**: Hangi değişiklikler önemli ve neden?
4. **Yazar Katkısı**: Kim ne zaman ne yaptı?
5. **Mimari Değişiklikler**: Yapısal değişiklikler var mı?
6. **Güvenlik Notları**: Güvenle ilgili değişiklikler var mı?
7. **Bugün**: Dosyanın mevcut durumu ve potansiyel sorunlar
8. **Öneriler**: Gelecekte yapılması gerekenler

Raporu Markdown formatında ve Türkçe yaz."""

        return await self.llm.generate(prompt, "Sen bir kod arkeoloğusun. Verilen dosya geçmişini analiz ederek kapsamlı bir arkeolojik rapor oluştur.")

    def _markdown_to_html(self, markdown_content: str) -> str:
        html_body = markdown.markdown(
            markdown_content,
            extensions=['extra', 'codehilite', 'toc'],
        )

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Arkeoloji Raporu</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        h1 {{ font-size: 2rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }}
        h2 {{ font-size: 1.5rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.25rem; }}
        code {{
            background-color: #f3f4f6;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SF Mono', Consolas, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #1f2937;
            color: #e5e7eb;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
            color: inherit;
        }}
        blockquote {{
            border-left: 4px solid #6366f1;
            margin-left: 0;
            padding-left: 1rem;
            color: #6b7280;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 0.5rem 1rem;
            text-align: left;
        }}
        th {{
            background-color: #f9fafb;
            font-weight: 600;
        }}
        a {{
            color: #6366f1;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
