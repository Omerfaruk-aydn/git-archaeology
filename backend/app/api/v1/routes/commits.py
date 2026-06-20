from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.git_service import GitService
from app.services.llm_service import LLMService
from app.models.repository import Repository, Commit
from app.schemas.repository import CommitResponse, CommitDetailResponse, FileChangeResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/commits", tags=["commits"])


@router.get("/")
async def list_commits(
    repo_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    author: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    query = db.query(Commit).filter(Commit.repository_id == str(repo_id))

    if author:
        query = query.filter(Commit.author_name.ilike(f"%{author}%"))

    total = query.count()
    commits = query.order_by(Commit.author_date.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": [CommitResponse.model_validate(c) for c in commits],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{commit_sha}", response_model=CommitDetailResponse)
async def get_commit(
    commit_sha: str,
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == str(repo_id),
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadi")

    return CommitDetailResponse.model_validate(commit)


@router.post("/{commit_sha}/analyze")
async def analyze_commit(
    commit_sha: str,
    repo_id: str,
    focus_areas: list[str] = Query(default=["security", "performance"]),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == str(repo_id),
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadi")

    repo = db.query(Repository).filter(Repository.id == str(repo_id)).first()
    if not repo or not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo yerel yolu bulunamadi")

    git_service = GitService(repo.local_path)
    llm_service = LLMService(provider="openrouter")

    file_changes = git_service.get_file_changes(commit_sha, include_diff=True)

    result = await llm_service.analyze_commit(
        commit_message=commit.message,
        file_changes=[fc.model_dump() for fc in file_changes],
        focus_areas=focus_areas,
    )

    commit.analysis_result = result
    commit.analyzed = True
    db.commit()

    return {"status": "success", "analysis": result}


@router.get("/{commit_sha}/explain")
async def explain_change(
    commit_sha: str,
    file_path: str,
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == str(repo_id),
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadi")

    repo = db.query(Repository).filter(Repository.id == str(repo_id)).first()
    if not repo or not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo yerel yolu bulunamadi")

    git_service = GitService(repo.local_path)
    llm_service = LLMService(provider="openrouter")

    old_content = git_service.get_file_content_at_commit(commit.parents[0] if commit.parents else "", file_path)
    new_content = git_service.get_file_content_at_commit(commit_sha, file_path)

    explanation = await llm_service.explain_change(
        old_code=old_content or "",
        new_code=new_content or "",
        commit_message=commit.message,
        file_path=file_path,
    )

    return {"explanation": explanation}
