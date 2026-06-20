from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.services.git_service import GitService
from app.services.analysis_engine import AnalysisEngine
from app.services.llm_service import LLMService
from app.models.repository import Repository, Analysis
from app.schemas.repository import (
    AnalysisCreate, AnalysisResponse, AnalysisResult,
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/analyses", tags=["analyses"])


async def run_analysis_background(analysis_id, repo_id, config: dict):
    import logging
    from datetime import datetime
    log = logging.getLogger(__name__)
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        repo = db.query(Repository).filter(Repository.id == str(repo_id)).first()
        if not repo:
            log.error(f"Depo bulunamadi: {repo_id}")
            return
        if not repo.local_path:
            log.error(f"Depo klonlanmamis: {repo_id}")
            a = db.query(Analysis).filter(Analysis.id == str(analysis_id)).first()
            if a:
                a.status = "failed"
                a.error_message = "Depo klonlanmamis"
                db.commit()
            return

        analysis = db.query(Analysis).filter(Analysis.id == str(analysis_id)).first()
        if not analysis:
            log.error(f"Analiz bulunamadi: {analysis_id}")
            return

        analysis.status = "running"
        analysis.started_at = datetime.utcnow()
        db.commit()

        git_service = GitService(repo.local_path)
        llm_service = LLMService(
            provider=config.get("llm_provider", "openai"),
            model=config.get("llm_model"),
        )

        engine = AnalysisEngine(db, git_service, llm_service)
        await engine.run_existing_analysis(repo, analysis, config)
    except Exception as e:
        log.error(f"Analiz hatasi: {e}", exc_info=True)
        try:
            a = db.query(Analysis).filter(Analysis.id == str(analysis_id)).first()
            if a:
                a.status = "failed"
                a.error_message = str(e)
                db.commit()
        except:
            pass
    finally:
        db.close()


@router.get("/")
async def list_analyses(
    repo_id: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Analysis).join(Repository).filter(
        Repository.owner_id == str(current_user.id)
    )

    if repo_id:
        query = query.filter(Analysis.repository_id == str(repo_id))
    if status:
        query = query.filter(Analysis.status == status)

    total = query.count()
    analyses = query.order_by(Analysis.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": [AnalysisResponse.model_validate(a) for a in analyses],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/", response_model=AnalysisResponse, status_code=201)
async def start_analysis(
    data: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(data.repository_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    if not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo once klonlanmali")

    config_data = data.model_dump()
    config_data["repository_id"] = str(config_data["repository_id"])

    analysis = Analysis(
        repository_id=repo.id,
        status="pending",
        config=config_data,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    background_tasks.add_task(
        run_analysis_background,
        analysis.id,
        repo.id,
        config_data,
    )

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == str(analysis_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadi")

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}/result", response_model=AnalysisResult)
async def get_analysis_result(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == str(analysis_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadi")

    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail=f"Analiz henuz tamamlanmadi: {analysis.status}")

    result = analysis.result
    if isinstance(result, str):
        import json
        result = json.loads(result)
    if not result:
        result = {}

    llm = result.get("llm_summary") or {}

    repo = db.query(Repository).filter(Repository.id == str(analysis.repository_id)).first()
    repo_name = repo.name if repo else "bilinmeyen"

    from app.models.repository import Commit, FileChange
    from collections import defaultdict

    commits = db.query(Commit).filter(
        Commit.repository_id == str(analysis.repository_id),
    ).all()

    author_stats = defaultdict(lambda: {"name": "", "commits": 0, "additions": 0, "deletions": 0})
    for c in commits:
        a = author_stats[c.author_name]
        a["name"] = c.author_name
        a["commits"] += 1
        a["additions"] += c.additions
        a["deletions"] += c.deletions
    author_contributions = sorted(author_stats.values(), key=lambda x: x["commits"], reverse=True)

    file_changes = db.query(FileChange).join(Commit).filter(
        Commit.repository_id == str(analysis.repository_id),
    ).all()
    file_freq = defaultdict(lambda: {"path": "", "changes": 0, "additions": 0, "deletions": 0})
    for fc in file_changes:
        f = file_freq[fc.file_path]
        f["path"] = fc.file_path
        f["changes"] += 1
        f["additions"] += fc.additions
        f["deletions"] += fc.deletions
    file_hotspots = sorted(file_freq.values(), key=lambda x: x["changes"], reverse=True)[:20]

    return AnalysisResult(
        analysis_id=str(analysis.id),
        repository_name=repo_name,
        summary=llm.get("overall_summary", ""),
        time_period=result.get("date_range", {}),
        statistics={
            "total_commits": result.get("total_commits", 0),
            "total_additions": result.get("total_additions", 0),
            "total_deletions": result.get("total_deletions", 0),
        },
        key_changes=file_hotspots,
        author_contributions=author_contributions,
        file_hotspots=file_hotspots,
        insights=llm.get("key_trends", []) + llm.get("potential_risks", []),
        recommendations=llm.get("recommendations", []),
    )


@router.delete("/{analysis_id}", status_code=204)
async def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == str(analysis_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadi")

    db.delete(analysis)
    db.commit()
