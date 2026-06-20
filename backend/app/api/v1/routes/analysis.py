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


async def run_analysis_background(analysis_id: uuid.UUID, repo_id: uuid.UUID, config: dict):
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        repo = db.query(Repository).filter(Repository.id == repo_id).first()
        if not repo or not repo.local_path:
            return

        git_service = GitService(repo.local_path)
        llm_service = LLMService(
            provider=config.get("llm_provider", "openai"),
            model=config.get("llm_model"),
        )

        analysis_config = AnalysisCreate(**config)
        engine = AnalysisEngine(db, git_service, llm_service)
        await engine.run_full_analysis(repo, analysis_config)
    finally:
        db.close()


@router.get("/")
async def list_analyses(
    repo_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Analysis).join(Repository).filter(
        Repository.owner_id == current_user.id
    )

    if repo_id:
        query = query.filter(Analysis.repository_id == repo_id)
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
        Repository.id == data.repository_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    if not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo önce klonlanmalı")

    analysis = Analysis(
        repository_id=repo.id,
        status="pending",
        config=data.model_dump(),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    background_tasks.add_task(
        run_analysis_background,
        analysis.id,
        repo.id,
        data.model_dump(),
    )

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == analysis_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}/result", response_model=AnalysisResult)
async def get_analysis_result(
    analysis_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == analysis_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")

    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail=f"Analiz henüz tamamlanmadı: {analysis.status}")

    return AnalysisResult(
        analysis_id=analysis.id,
        repository_name=analysis.repository.name,
        summary=analysis.result.get("llm_summary", {}).get("overall_summary", ""),
        time_period=analysis.result.get("date_range", {}),
        statistics={
            "total_commits": analysis.result.get("total_commits", 0),
            "total_additions": analysis.result.get("total_additions", 0),
            "total_deletions": analysis.result.get("total_deletions", 0),
        },
        key_changes=analysis.result.get("top_files", []),
        author_contributions=[],
        file_hotspots=analysis.result.get("top_files", []),
        insights=analysis.result.get("llm_summary", {}).get("key_trends", []),
        recommendations=analysis.result.get("llm_summary", {}).get("recommendations", []),
    )


@router.delete("/{analysis_id}", status_code=204)
async def delete_analysis(
    analysis_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analysis = db.query(Analysis).join(Repository).filter(
        Analysis.id == analysis_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı")

    db.delete(analysis)
    db.commit()
