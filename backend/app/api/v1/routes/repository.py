from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.git_service import GitService
from app.models.repository import Repository
from app.schemas.repository import (
    RepositoryCreate, RepositoryUpdate, RepositoryResponse,
    RepositoryList,
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("/", response_model=RepositoryList)
async def list_repositories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Repository).filter(Repository.owner_id == str(current_user.id))

    if search:
        query = query.filter(Repository.name.ilike(f"%{search}%"))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return RepositoryList(
        items=[RepositoryResponse.model_validate(r) for r in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=RepositoryResponse, status_code=201)
async def create_repository(
    data: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = db.query(Repository).filter(Repository.url == data.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu URL zaten kayitli")

    repo = Repository(
        name=data.name,
        url=data.url,
        local_path=data.local_path,
        default_branch=data.default_branch,
        description=data.description,
        owner_id=str(current_user.id),
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)

    return RepositoryResponse.model_validate(repo)


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    return RepositoryResponse.model_validate(repo)


@router.put("/{repo_id}", response_model=RepositoryResponse)
async def update_repository(
    repo_id: str,
    data: RepositoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(repo, key, value)

    db.commit()
    db.refresh(repo)

    return RepositoryResponse.model_validate(repo)


@router.delete("/{repo_id}", status_code=204)
async def delete_repository(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    db.delete(repo)
    db.commit()


@router.post("/{repo_id}/clone")
async def clone_repository(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    if repo.local_path:
        raise HTTPException(status_code=400, detail="Depo zaten klonlanmis")

    try:
        target_dir = f"C:/proje/repos/{repo.id}"
        import subprocess
        subprocess.run(["git", "clone", repo.url, target_dir], check=True, timeout=60)
        repo.local_path = target_dir
        db.commit()

        return {"status": "success", "local_path": target_dir}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{repo_id}/sync")
async def sync_repository(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == str(repo_id),
        Repository.owner_id == str(current_user.id),
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadi")

    if not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo once klonlanmali")

    git_service = GitService(repo.local_path)
    success = git_service.pull_latest(repo.default_branch)

    if success:
        repo.last_analyzed_at = None
        repo.is_analyzed = False
        db.commit()
        return {"status": "synced"}
    else:
        raise HTTPException(status_code=500, detail="Senkronizasyon basarisiz")
