from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.services.report_service import ReportService
from app.services.llm_service import LLMService
from app.models.repository import Repository
from app.schemas.repository import ReportRequest, ReportResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=ReportResponse, status_code=201)
async def generate_report(
    data: ReportRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == data.repository_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    llm_service = LLMService(provider="openai")
    report_service = ReportService(db, llm_service)

    try:
        result = await report_service.generate_report(
            repository_id=str(data.repository_id),
            report_type=data.report_type,
            branch=data.branch,
            start_date=data.start_date,
            end_date=data.end_date,
            file_paths=data.file_paths,
            format=data.format,
        )

        from datetime import datetime
        report = ReportResponse(
            id=uuid.uuid4(),
            repository_id=data.repository_id,
            report_type=data.report_type,
            content=result["content"],
            format=result["format"],
            generated_at=datetime.utcnow(),
            metadata=result.get("metadata"),
        )

        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{repo_id}/archeological/{file_path:path}")
async def get_archeological_report(
    repo_id: uuid.UUID,
    file_path: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    llm_service = LLMService(provider="openai")
    report_service = ReportService(db, llm_service)

    try:
        content = await report_service.generate_archeological_report(
            repository_id=str(repo_id),
            file_path=file_path,
        )

        return {"content": content, "format": "markdown"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
