# Git Arkeoloji Aracı — Full Stack Proje Promptu

## 1. Proje Tanımı

**Ad:** Git Arkeoloji Aracı (GitArch)
**Amaç:** Git depo geçmişini analiz ederek kodun neden, ne zaman ve kim tarafından değiştirildiğini anlayan, bunu doğal dilde açıklayan bir araç. Legacy kod tabanları için "arkeolojik rapor" üretir.
**Hedef Kullanıcı:** Yazılım geliştiriciler, devops mühendisleri, teknik liderler, kod inceleme ekipleri.
**Platform:** Web tabanlı (backend API + frontend SPA). CLI fallback mevcut.

---

## 2. Mimari Kararlar

### 2.1 Teknoloji Yığını

| Katman | Teknoloji | Sebep |
|--------|-----------|-------|
| Backend | Python 3.11+ (FastAPI) | GitPython kütüphanesiyle doğal entegrasyon, async support, OpenAPI spec üretimi |
| Veritabanı | PostgreSQL 16 + SQLAlchemy 2.0 | Relational veri modeli, JSONB desteği,全文 arama |
| Cache | Redis 7 | Analiz sonuçlarını cacheleme, job queue |
| Celery | Celery 5 + Redis broker | Arka plan analiz jobları |
| Frontend | React 18 + TypeScript + Vite | Type safety, hızlı geliştirme, modern toolchain |
| UI | Tailwind CSS + Headless UI | Utility-first, erişilebilir, glassmorphism'sız |
| LLM Entegrasyon | OpenAI GPT-4o / Claude 3.5 Sonnet / yerel modeller | Konfigüre edilebilir LLM provider |
| Auth | JWT + OAuth2 (GitHub/GitLab) | SSO entegrasyonu |
| Deployment | Docker Compose / Kubernetes | Both local dev and production |

### 2.2 Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Dashboard │  │ Analiz   │  │ Rapor    │  │ Ayarlar │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │ REST API
┌───────────────────────┴─────────────────────────────────┐
│                  Backend (FastAPI)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Repo     │  │ Analiz   │  │ Rapor    │  │ Auth    │ │
│  │ Manager  │  │ Engine   │  │ Builder  │  │ Service │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Git      │  │ LLM      │  │ Queue    │              │
│  │ Service  │  │ Service  │  │ Worker   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────┐
│                    Data Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │PostgreSQL│  │  Redis   │  │  Git     │              │
│  │          │  │          │  │  Repos   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Veri Modelleri

### 3.1 SQLAlchemy Modelleri

```python
# models/repository.py

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    Boolean, Float, JSON, Enum as SAEnum, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    local_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    default_branch: Mapped[str] = mapped_column(String(255), default="main")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_analyzed: Mapped[bool] = mapped_column(Boolean, default=False)
    last_analyzed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    commits: Mapped[List["Commit"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    branches: Mapped[List["Branch"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    analyses: Mapped[List["Analysis"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    file_snapshots: Mapped[List["FileSnapshot"]] = relationship(back_populates="repository", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_repositories_owner_id", "owner_id"),
        Index("ix_repositories_url", "url", unique=True),
    )


class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("repositories.id"))
    sha: Mapped[str] = mapped_column(String(40), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    author_email: Mapped[str] = mapped_column(String(255), nullable=False)
    author_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    committer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    committer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    committer_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    parents: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    files_changed: Mapped[int] = mapped_column(Integer, default=0)
    analyzed: Mapped[bool] = mapped_column(Boolean, default=False)
    analysis_result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    repository: Mapped["Repository"] = relationship(back_populates="commits")
    file_changes: Mapped[List["FileChange"]] = relationship(back_populates="commit", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_commits_repository_id", "repository_id"),
        Index("ix_commits_sha", "sha"),
        Index("ix_commits_author_date", "author_date"),
        Index("ix_commits_analyzed", "analyzed"),
    )


class FileChange(Base):
    __tablename__ = "file_changes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("commits.id"))
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    old_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False)  # modified, added, deleted, renamed
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    diff: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    old_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    analysis: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    commit: Mapped["Commit"] = relationship(back_populates="file_changes")

    __table_args__ = (
        Index("ix_file_changes_commit_id", "commit_id"),
        Index("ix_file_changes_file_path", "file_path"),
    )


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("repositories.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    head_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    repository: Mapped["Repository"] = relationship(back_populates="branches")

    __table_args__ = (
        Index("ix_branches_repository_id", "repository_id"),
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("repositories.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, running, completed, failed
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    total_commits: Mapped[int] = mapped_column(Integer, default=0)
    processed_commits: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    repository: Mapped["Repository"] = relationship(back_populates="analyses")

    __table_args__ = (
        Index("ix_analyses_repository_id", "repository_id"),
        Index("ix_analyses_status", "status"),
    )


class FileSnapshot(Base):
    __tablename__ = "file_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("repositories.id"))
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    repository: Mapped["Repository"] = relationship(back_populates="file_snapshots")

    __table_args__ = (
        Index("ix_file_snapshots_repo_file", "repository_id", "file_path"),
        Index("ix_file_snapshots_content_hash", "content_hash"),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)  # nullable for OAuth
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    oauth_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    oauth_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    repositories: Mapped[List["Repository"]] = relationship(back_populates="owner")

    __table_args__ = (
        Index("ix_users_email", "email"),
    )
```

### 3.2 Pydantic Şemaları

```python
# schemas/repository.py

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict
import uuid


# === Repository Schemas ===

class RepositoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., max_length=1024)
    default_branch: str = Field(default="main", max_length=255)
    description: Optional[str] = None
    local_path: Optional[str] = None


class RepositoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    default_branch: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    url: str
    local_path: Optional[str]
    default_branch: str
    description: Optional[str]
    is_analyzed: bool
    last_analyzed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    commit_count: Optional[int] = None
    contributor_count: Optional[int] = None


class RepositoryList(BaseModel):
    items: List[RepositoryResponse]
    total: int
    page: int
    page_size: int


# === Commit Schemas ===

class CommitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sha: str
    message: str
    author_name: str
    author_email: str
    author_date: datetime
    additions: int
    deletions: int
    files_changed: int
    analyzed: bool
    analysis_result: Optional[dict]


class CommitDetailResponse(CommitResponse):
    parents: Optional[list]
    committer_name: str
    committer_email: str
    committer_date: datetime
    file_changes: List["FileChangeResponse"] = []


# === FileChange Schemas ===

class FileChangeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    file_path: str
    old_path: Optional[str]
    change_type: str
    additions: int
    deletions: int
    analysis: Optional[dict]


class FileChangeDetailResponse(FileChangeResponse):
    diff: Optional[str]


# === Analysis Schemas ===

class AnalysisCreate(BaseModel):
    repository_id: uuid.UUID
    branch: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_commits: Optional[int] = Field(None, ge=1, le=100000)
    llm_provider: str = Field(default="openai", pattern="^(openai|anthropic|local)$")
    llm_model: str = Field(default="gpt-4o")
    focus_areas: Optional[List[str]] = None  # security, performance, architecture, etc.
    include_diffs: bool = Field(default=True)
    batch_size: int = Field(default=10, ge=1, le=50)


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_id: uuid.UUID
    status: str
    progress: float
    total_commits: int
    processed_commits: int
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime


class AnalysisResult(BaseModel):
    analysis_id: uuid.UUID
    repository_name: str
    summary: str
    time_period: dict
    statistics: dict
    key_changes: List[dict]
    author_contributions: List[dict]
    file_hotspots: List[dict]
    insights: List[dict]
    recommendations: List[str]


# === Report Schemas ===

class ReportRequest(BaseModel):
    repository_id: uuid.UUID
    report_type: str = Field(..., pattern="^(full|summary|security|architecture|legacy)$")
    branch: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    file_paths: Optional[List[str]] = None
    format: str = Field(default="markdown", pattern="^(markdown|html|pdf)$")


class ReportResponse(BaseModel):
    id: uuid.UUID
    repository_id: uuid.UUID
    report_type: str
    content: str
    format: str
    generated_at: datetime
    metadata: Optional[dict]


# === Auth Schemas ===

class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None
```

---

## 4. Backend — Servis Katmanı

### 4.1 Git Servisi

```python
# services/git_service.py

import os
import subprocess
import json
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import logging

from git import Repo, GitCommandError, InvalidGitRepositoryError
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GitCommitInfo(BaseModel):
    sha: str
    message: str
    author_name: str
    author_email: str
    author_date: datetime
    committer_name: str
    committer_email: str
    committer_date: datetime
    parents: List[str]
    additions: int = 0
    deletions: int = 0
    files_changed: int = 0


class GitFileChange(BaseModel):
    file_path: str
    old_path: Optional[str] = None
    change_type: str
    additions: int = 0
    deletions: int = 0
    diff: Optional[str] = None
    old_content: Optional[str] = None
    new_content: Optional[str] = None


class GitService:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self._repo: Optional[Repo] = None

    @property
    def repo(self) -> Repo:
        if self._repo is None:
            try:
                self._repo = Repo(self.repo_path)
            except InvalidGitRepositoryError:
                raise ValueError(f"Geçersiz Git deposu: {self.repo_path}")
        return self._repo

    def validate_repo(self) -> bool:
        try:
            _ = self.repo
            return True
        except (InvalidGitRepositoryError, ValueError):
            return False

    def get_repo_info(self) -> Dict[str, Any]:
        repo = self.repo
        branches = [b.name for b in repo.branches]
        remote_url = ""
        if repo.remotes:
            remote_url = str(repo.remotes[0].url)

        return {
            "path": str(self.repo_path),
            "bare": repo.bare,
            "branches": branches,
            "current_branch": str(repo.active_branch) if not repo.head.is_detached else "HEAD detached",
            "remote_url": remote_url,
            "head_sha": str(repo.head.commit.hexsha),
            "is_dirty": repo.is_dirty(),
        }

    def get_commits(
        self,
        branch: str = "main",
        max_count: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        author: Optional[str] = None,
    ) -> List[GitCommitInfo]:
        repo = self.repo

        try:
            if branch not in [b.name for b in repo.branches]:
                # Try as remote branch
                ref = f"origin/{branch}"
                if ref not in [str(r) for r in repo.refs]:
                    raise ValueError(f"Bulunamadı: {branch}")
        except Exception:
            pass

        cmd_parts = ["--format=%H|%s|%an|%ae|%ai|%cn|%ce|%ci|%P"]

        if max_count:
            cmd_parts.append(f"--max-count={max_count}")

        if start_date:
            cmd_parts.append(f"--since={start_date.isoformat()}")

        if end_date:
            cmd_parts.append(f"--until={end_date.isoformat()}")

        if author:
            cmd_parts.append(f"--author={author}")

        cmd_parts.append(branch)

        commits = []
        try:
            output = repo.git.log(*cmd_parts)
        except GitCommandError as e:
            logger.error(f"Git log hatası: {e}")
            return []

        for line in output.strip().split("\n"):
            if not line.strip():
                continue

            parts = line.split("|", 8)
            if len(parts) < 9:
                continue

            sha, message, author_name, author_email, author_date_str, \
                committer_name, committer_email, committer_date_str, parents_str = parts

            try:
                author_date = datetime.fromisoformat(author_date_str.strip())
                committer_date = datetime.fromisoformat(committer_date_str.strip())
            except ValueError:
                continue

            parents = [p.strip() for p in parents_str.split() if p.strip()]

            commits.append(GitCommitInfo(
                sha=sha.strip(),
                message=message.strip(),
                author_name=author_name.strip(),
                author_email=author_email.strip(),
                author_date=author_date,
                committer_name=committer_name.strip(),
                committer_email=committer_email.strip(),
                committer_date=committer_date,
                parents=parents,
            ))

        return commits

    def get_commit_stats(self, sha: str) -> Dict[str, int]:
        repo = self.repo
        try:
            commit = repo.commit(sha)
            stats = commit.stats
            return {
                "total": stats.total["lines"],
                "insertions": stats.total["insertions"],
                "deletions": stats.total["deletions"],
                "files_changed": len(stats.files),
            }
        except Exception as e:
            logger.error(f"Commit stats hatası ({sha}): {e}")
            return {"total": 0, "insertions": 0, "deletions": 0, "files_changed": 0}

    def get_file_changes(self, sha: str, include_diff: bool = True) -> List[GitFileChange]:
        repo = self.repo
        changes = []

        try:
            commit = repo.commit(sha)

            if len(commit.parents) == 0:
                # First commit — all files are additions
                for item in commit.tree.traverse():
                    if item.type == "blob":
                        try:
                            content = item.data_stream.read().decode("utf-8", errors="replace")
                            lines = content.count("\n") + 1
                            changes.append(GitFileChange(
                                file_path=item.path,
                                change_type="added",
                                additions=lines,
                                deletions=0,
                                new_content=content if include_diff else None,
                            ))
                        except Exception:
                            changes.append(GitFileChange(
                                file_path=item.path,
                                change_type="added",
                            ))
            else:
                diff = commit.parents[0].diff(commit)
                for d in diff:
                    file_path = d.b_path or d.a_path
                    change_type = "modified"

                    if d.new_file:
                        change_type = "added"
                    elif d.deleted_file:
                        change_type = "deleted"
                    elif d.renamed_file:
                        change_type = "renamed"

                    additions = 0
                    deletions = 0
                    diff_content = None
                    old_content = None
                    new_content = None

                    if include_diff and change_type != "deleted":
                        try:
                            diff_content = d.diff.decode("utf-8", errors="replace")
                            additions = diff_content.count("+") - diff_content.count("++")
                            deletions = diff_content.count("-") - diff_content.count("--")
                        except Exception:
                            pass

                    if include_diff:
                        try:
                            if change_type != "deleted":
                                new_content = repo.git.show(f"{sha}:{file_path}")
                            if change_type != "added":
                                old_content = repo.git.show(f"{commit.parents[0].hexsha}:{d.a_path}")
                        except Exception:
                            pass

                    changes.append(GitFileChange(
                        file_path=file_path,
                        old_path=d.a_path if d.renamed_file else None,
                        change_type=change_type,
                        additions=max(0, additions),
                        deletions=max(0, deletions),
                        diff=diff_content,
                        old_content=old_content,
                        new_content=new_content,
                    ))

        except Exception as e:
            logger.error(f"File changes hatası ({sha}): {e}")

        return changes

    def get_file_content_at_commit(self, sha: str, file_path: str) -> Optional[str]:
        repo = self.repo
        try:
            return repo.git.show(f"{sha}:{file_path}")
        except Exception:
            return None

    def get_file_blame(self, file_path: str, commit_sha: Optional[str] = None) -> List[Dict[str, Any]]:
        repo = self.repo
        ref = commit_sha or "HEAD"

        try:
            blame_output = repo.git.blame("-p", ref, "--", file_path)
            lines = blame_output.strip().split("\n")

            result = []
            current_commit = None
            current_author = None
            current_date = None

            for line in lines:
                if line.startswith("^"):
                    # First commit in blame
                    parts = line[1:].split()
                    current_commit = parts[0] if parts else None
                elif not line.startswith("\t") and len(line.split()) >= 3:
                    parts = line.split()
                    current_commit = parts[0]
                    current_author = " ".join(parts[1:-2])
                elif line.startswith("\t"):
                    content = line[1:]
                    result.append({
                        "commit": current_commit,
                        "author": current_author,
                        "content": content,
                    })

            return result
        except Exception as e:
            logger.error(f"Blame hatası ({file_path}): {e}")
            return []

    def get_file_history(self, file_path: str, max_count: Optional[int] = None) -> List[Dict[str, Any]]:
        repo = self.repo
        cmd = ["--format=%H|%s|%an|%ai", f"--follow", "-p", "--", file_path]

        if max_count:
            cmd.append(f"--max-count={max_count}")

        try:
            output = repo.git.log(*cmd)
            commits = []
            for line in output.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    commits.append({
                        "sha": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3],
                    })
            return commits
        except Exception as e:
            logger.error(f"File history hatası ({file_path}): {e}")
            return []

    def get_directory_tree(self, sha: str = "HEAD", path: str = "") -> List[Dict[str, Any]]:
        repo = self.repo
        tree = repo.commit(sha).tree

        if path:
            tree = tree[path]

        result = []
        for item in tree.traverse():
            result.append({
                "path": item.path,
                "type": item.type,
                "size": getattr(item, "size", 0),
                "sha": item.hexsha,
            })

        return result

    def clone_repo(self, url: str, target_dir: str, branch: Optional[str] = None) -> str:
        try:
            cmd = ["git", "clone", "--depth=1"]
            if branch:
                cmd.extend(["--branch", branch])
            cmd.extend([url, target_dir])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return target_dir
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Clone hatası: {e.stderr}")

    def pull_latest(self, branch: Optional[str] = None) -> bool:
        repo = self.repo
        try:
            remote = repo.remotes.origin
            if branch:
                remote.pull(branch)
            else:
                remote.pull()
            return True
        except Exception as e:
            logger.error(f"Pull hatası: {e}")
            return False
```

### 4.2 Analiz Motoru

```python
# services/analysis_engine.py

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

            # Process commits in batches
            for i in range(0, len(commits), config.batch_size):
                batch = commits[i:i + config.batch_size]
                await self._process_commit_batch(batch, analysis, config)
                analysis.processed_commits = i + len(batch)
                analysis.progress = (i + len(batch)) / len(commits) * 100
                self.db.commit()

            # Generate summary
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
            # Check if commit already analyzed
            existing = self.db.query(Commit).filter(
                Commit.sha == commit_info.sha,
                Commit.analyzed == True,
            ).first()

            if existing:
                continue

            # Get or create commit record
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

            # Get file changes
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

            # LLM analysis for this commit
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

        for fc in file_changes[:20]:  # Limit to 20 files
            prompt += f"\n- {fc.file_path} ({fc.change_type}): +{fc.additions} -{fc.deletions}"
            if fc.diff:
                # Truncate long diffs
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

        # Calculate statistics
        total_additions = sum(c.additions for c in commits)
        total_deletions = sum(c.deletions for c in commits)
        unique_authors = list(set(c.author_name for c in commits))

        # File hotspot analysis
        file_changes = self.db.query(FileChange).join(Commit).filter(
            Commit.repository_id == repo.id,
        ).all()

        file_frequency = defaultdict(int)
        for fc in file_changes:
            file_frequency[fc.file_path] += 1

        top_files = sorted(file_frequency.items(), key=lambda x: x[1], reverse=True)[:20]

        # Category analysis
        categories = defaultdict(int)
        for commit in commits:
            if commit.analysis_result and "category" in commit.analysis_result:
                categories[commit.analysis_result["category"]] += 1

        # Time-based analysis
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

        # Generate LLM summary
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
```

### 4.3 LLM Servisi

```python
# services/llm_service.py

import json
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

import httpx
from openai import AsyncOpenAI
import anthropic

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=4000,
        )
        return response.choices[0].message.content

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)

        # Extract JSON from response
        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0]
            else:
                json_str = result

            return json.loads(json_str.strip())
        except json.JSONDecodeError:
            logger.warning(f"JSON parse hatası, ham yanıt döndürülüyor: {result[:200]}")
            return {"raw_response": result}


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = await self.client.messages.create(**kwargs)
        return response.content[0].text

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        json_system = (system_prompt or "") + "\n\nYanıtını her zaman geçerli JSON formatında ver."
        result = await self.generate(prompt, json_system)

        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0]
            else:
                json_str = result

            return json.loads(json_str.strip())
        except json.JSONDecodeError:
            return {"raw_response": result}


class LocalProvider(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json()["response"]

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        result = await self.generate(prompt, system_prompt)

        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0]
            else:
                json_str = result

            return json.loads(json_str.strip())
        except json.JSONDecodeError:
            return {"raw_response": result}


class LLMService:
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        self.provider_name = provider

        if provider == "openai":
            self.provider = OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=model or settings.OPENAI_MODEL,
            )
        elif provider == "anthropic":
            self.provider = AnthropicProvider(
                api_key=settings.ANTHROPIC_API_KEY,
                model=model or settings.ANTHROPIC_MODEL,
            )
        elif provider == "local":
            self.provider = LocalProvider(
                base_url=settings.LOCAL_LLM_URL,
                model=model or settings.LOCAL_LLM_MODEL,
            )
        else:
            raise ValueError(f"Desteklenmeyen LLM provider: {provider}")

    async def analyze_commit(
        self,
        commit_message: str,
        file_changes: List[Dict[str, Any]],
        focus_areas: List[str],
    ) -> Dict[str, Any]:
        system_prompt = """Sen bir Git arkeoloğu ve kod analiz uzmanısın.
Görevin, Git commit'lerini analiz ederek:
- Kodun neden değiştiğini anlamak
- Değişikliklerin etkilerini değerlendirmek
- Güvenlik, performans ve mimari riskleri tespit etmek
- Gelecekteki bakım için ipuçları sağlamak

Yanıtların her zaman JSON formatında olmalı ve Türkçe yazılmalı."""

        focus_str = ", ".join(focus_areas)
        files_summary = "\n".join([
            f"- {fc.get('file_path', 'unknown')} ({fc.get('change_type', 'unknown')}): +{fc.get('additions', 0)} -{fc.get('deletions', 0)}"
            for fc in file_changes[:15]
        ])

        prompt = f"""Bu commit'u analiz et:

Commit Mesajı: {commit_message}

Değişen Dosyalar:
{files_summary}

Odak Alanları: {focus_str}

Lütfen şu JSON yapısında yanıt ver:
{{
  "summary": "Bu commit'un kısa özeti (1-2 cümle)",
  "category": "security|performance|architecture|dependency|refactor|feature|bugfix|other",
  "importance": "high|medium|low",
  "tags": ["ilgili etiketler"],
  "insights": ["Bu değişiklikle ilgili önemli gözlemler"],
  "related_files": ["İlişkili dosya yolları"],
  "potential_issues": ["Olası sorunlar veya riskler"],
  "recommendations": ["Öneriler"]
}}"""

        return await self.provider.generate_json(prompt, system_prompt)

    async def generate_summary(self, prompt: str) -> Dict[str, Any]:
        system_prompt = """Sen bir Git arkeoloğu ve raporlama uzmanısın.
Verilen analiz sonuçlarını kullanarak kapsamlı ve anlamlı özetler oluştur.
Yanıtların her zaman JSON formatında olmalı ve Türkçe yazılmalı."""

        return await self.provider.generate_json(prompt, system_prompt)

    async def generate_report(self, analysis_data: Dict[str, Any], report_type: str) -> str:
        system_prompt = """Sen bir teknik rapor yazarısın.
Verilen analiz sonuçlarını kullanarak profesyonel ve detaylı raporlar oluştur.
Raporlar Markdown formatında ve Türkçe olmalı."""

        prompts = {
            "full": "Kapsamlı bir arkeolojik analiz raporu oluştur",
            "summary": "Kısa bir özet rapor oluştur",
            "security": "Güvenlik odaklı bir rapor oluştur",
            "architecture": "Mimari analiz raporu oluştur",
            "legacy": "Legacy kod analiz raporu oluştur",
        }

        prompt = f"""{prompts.get(report_type, 'Genel bir rapor oluştur')}

Analiz Verileri:
{json.dumps(analysis_data, indent=2, ensure_ascii=False)}

Raporu şu bölümlerle oluştur:
1. Yönetici Özeti
2. Genel Bakış
3. Detaylı Analiz Bulguları
4. Risk Değerlendirmesi
5. Öneriler
6. Sonuç"""

        return await self.provider.generate(prompt, system_prompt)

    async def explain_change(
        self,
        old_code: str,
        new_code: str,
        commit_message: str,
        file_path: str,
    ) -> str:
        system_prompt = """Sen bir kod arkeoloğusun.
İki kod sürümü arasındaki farkları açıkça ve detaylı şekilde açıkla.
Neden böyle bir değişiklik yapılmış olabileceğini analiz et.
Türkçe yaz."""

        prompt = f"""Bu kod değişikliğini açıkla:

Dosya: {file_path}
Commit Mesajı: {commit_message}

Eski Kod:
```
{old_code[:3000]}
```

Yeni Kod:
```
{new_code[:3000]}
```

Bu değişikliği şu açılardan açıkla:
1. Ne değişti? (Somut değişiklikler)
2. Neden değişti? (Muhtemel sebepler)
3. Etkisi ne? (Kod üzerindeki etki)
4. Riskler neler? (Olası sorunlar)"""

        return await self.provider.generate(prompt, system_prompt)
```

### 4.4 API Rotaları

```python
# api/v1/routes/repository.py

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid

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
    query = db.query(Repository).filter(Repository.owner_id == current_user.id)

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
        raise HTTPException(status_code=400, detail="Bu URL zaten kayıtlı")

    repo = Repository(
        name=data.name,
        url=data.url,
        local_path=data.local_path,
        default_branch=data.default_branch,
        description=data.description,
        owner_id=current_user.id,
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)

    return RepositoryResponse.model_validate(repo)


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    return RepositoryResponse.model_validate(repo)


@router.put("/{repo_id}", response_model=RepositoryResponse)
async def update_repository(
    repo_id: uuid.UUID,
    data: RepositoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(repo, key, value)

    db.commit()
    db.refresh(repo)

    return RepositoryResponse.model_validate(repo)


@router.delete("/{repo_id}", status_code=204)
async def delete_repository(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    db.delete(repo)
    db.commit()


@router.post("/{repo_id}/clone")
async def clone_repository(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    if repo.local_path:
        raise HTTPException(status_code=400, detail="Depo zaten klonlanmış")

    try:
        git_service = GitService("")
        target_dir = f"/data/repos/{repo.id}"
        git_service.clone_repo(repo.url, target_dir, repo.default_branch)
        repo.local_path = target_dir
        db.commit()

        return {"status": "success", "local_path": target_dir}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{repo_id}/sync")
async def sync_repository(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    if not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo önce klonlanmalı")

    git_service = GitService(repo.local_path)
    success = git_service.pull_latest(repo.default_branch)

    if success:
        repo.last_analyzed_at = None
        repo.is_analyzed = False
        db.commit()
        return {"status": "synced"}
    else:
        raise HTTPException(status_code=500, detail="Senkronizasyon başarısız")
```

```python
# api/v1/routes/analysis.py

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


@router.get("/", response_model=list[AnalysisResponse])
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

    analyses = query.order_by(Analysis.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return [AnalysisResponse.model_validate(a) for a in analyses]


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
```

```python
# api/v1/routes/commits.py

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.services.git_service import GitService
from app.services.llm_service import LLMService
from app.models.repository import Repository, Commit
from app.schemas.repository import CommitResponse, CommitDetailResponse, FileChangeResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/commits", tags=["commits"])


@router.get("/", response_model=list[CommitResponse])
async def list_commits(
    repo_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    author: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.owner_id == current_user.id,
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Depo bulunamadı")

    query = db.query(Commit).filter(Commit.repository_id == repo_id)

    if author:
        query = query.filter(Commit.author_name.ilike(f"%{author}%"))

    commits = query.order_by(Commit.author_date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return [CommitResponse.model_validate(c) for c in commits]


@router.get("/{commit_sha}", response_model=CommitDetailResponse)
async def get_commit(
    commit_sha: str,
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == repo_id,
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadı")

    return CommitDetailResponse.model_validate(commit)


@router.post("/{commit_sha}/analyze")
async def analyze_commit(
    commit_sha: str,
    repo_id: uuid.UUID,
    focus_areas: list[str] = Query(default=["security", "performance"]),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == repo_id,
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadı")

    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo or not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo yerel yolu bulunamadı")

    git_service = GitService(repo.local_path)
    llm_service = LLMService(provider="openai")

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
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commit = db.query(Commit).filter(
        Commit.sha == commit_sha,
        Commit.repository_id == repo_id,
    ).first()

    if not commit:
        raise HTTPException(status_code=404, detail="Commit bulunamadı")

    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo or not repo.local_path:
        raise HTTPException(status_code=400, detail="Depo yerel yolu bulunamadı")

    git_service = GitService(repo.local_path)
    llm_service = LLMService(provider="openai")

    old_content = git_service.get_file_content_at_commit(commit.parents[0] if commit.parents else "", file_path)
    new_content = git_service.get_file_content_at_commit(commit_sha, file_path)

    explanation = await llm_service.explain_change(
        old_code=old_content or "",
        new_code=new_content or "",
        commit_message=commit.message,
        file_path=file_path,
    )

    return {"explanation": explanation}
```

---

## 5. Frontend

### 5.1 Proje Yapısı

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── repositories.ts
│   │   ├── analyses.ts
│   │   ├── commits.ts
│   │   └── reports.ts
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Layout.tsx
│   │   ├── repositories/
│   │   │   ├── RepositoryList.tsx
│   │   │   ├── RepositoryCard.tsx
│   │   │   ├── RepositoryForm.tsx
│   │   │   └── RepositoryDetail.tsx
│   │   ├── analysis/
│   │   │   ├── AnalysisList.tsx
│   │   │   ├── AnalysisForm.tsx
│   │   │   ├── AnalysisProgress.tsx
│   │   │   └── AnalysisResult.tsx
│   │   ├── commits/
│   │   │   ├── CommitList.tsx
│   │   │   ├── CommitDetail.tsx
│   │   │   ├── CommitTimeline.tsx
│   │   │   └── FileChangeView.tsx
│   │   ├── reports/
│   │   │   ├── ReportGenerator.tsx
│   │   │   └── ReportViewer.tsx
│   │   └── common/
│   │       ├── DataTable.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── DateRangePicker.tsx
│   ├── hooks/
│   │   ├── useRepository.ts
│   │   ├── useAnalysis.ts
│   │   ├── useCommits.ts
│   │   └── useDebounce.ts
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Repositories.tsx
│   │   ├── RepositoryDetail.tsx
│   │   ├── Analysis.tsx
│   │   ├── AnalysisDetail.tsx
│   │   ├── Commits.tsx
│   │   ├── Reports.tsx
│   │   ├── Settings.tsx
│   │   └── Login.tsx
│   ├── store/
│   │   ├── authStore.ts
│   │   └── uiStore.ts
│   ├── types/
│   │   └── index.ts
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
└── index.html
```

### 5.2 Tip Tanımları

```typescript
// types/index.ts

export interface Repository {
  id: string;
  name: string;
  url: string;
  local_path: string | null;
  default_branch: string;
  description: string | null;
  is_analyzed: boolean;
  last_analyzed_at: string | null;
  created_at: string;
  updated_at: string;
  commit_count?: number;
  contributor_count?: number;
}

export interface Commit {
  id: string;
  sha: string;
  message: string;
  author_name: string;
  author_email: string;
  author_date: string;
  additions: number;
  deletions: number;
  files_changed: number;
  analyzed: boolean;
  analysis_result: Record<string, any> | null;
}

export interface CommitDetail extends Commit {
  parents: string[];
  committer_name: string;
  committer_email: string;
  committer_date: string;
  file_changes: FileChange[];
}

export interface FileChange {
  id: string;
  file_path: string;
  old_path: string | null;
  change_type: 'added' | 'modified' | 'deleted' | 'renamed';
  additions: number;
  deletions: number;
  diff?: string;
  analysis?: Record<string, any>;
}

export interface Analysis {
  id: string;
  repository_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  total_commits: number;
  processed_commits: number;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface AnalysisResult {
  analysis_id: string;
  repository_name: string;
  summary: string;
  time_period: {
    start: string;
    end: string;
  };
  statistics: {
    total_commits: number;
    total_additions: number;
    total_deletions: number;
  };
  key_changes: Array<{
    path: string;
    changes: number;
  }>;
  author_contributions: Array<{
    name: string;
    commits: number;
    additions: number;
    deletions: number;
  }>;
  file_hotspots: Array<{
    path: string;
    changes: number;
  }>;
  insights: string[];
  recommendations: string[];
}

export interface Report {
  id: string;
  repository_id: string;
  report_type: string;
  content: string;
  format: string;
  generated_at: string;
  metadata: Record<string, any> | null;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface AnalysisConfig {
  repository_id: string;
  branch?: string;
  start_date?: string;
  end_date?: string;
  max_commits?: number;
  llm_provider: 'openai' | 'anthropic' | 'local';
  llm_model?: string;
  focus_areas?: string[];
  include_diffs?: boolean;
  batch_size?: number;
}
```

### 5.3 API İstemcisi

```typescript
// api/client.ts

import { AuthTokens } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private tokens: AuthTokens | null = null;

  setTokens(tokens: AuthTokens | null) {
    this.tokens = tokens;
    if (tokens) {
      localStorage.setItem('tokens', JSON.stringify(tokens));
    } else {
      localStorage.removeItem('tokens');
    }
  }

  getTokens(): AuthTokens | null {
    if (!this.tokens) {
      const stored = localStorage.getItem('tokens');
      if (stored) {
        this.tokens = JSON.parse(stored);
      }
    }
    return this.tokens;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const tokens = this.getTokens();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options.headers as Record<string, string>) || {}),
    };

    if (tokens?.access_token) {
      headers['Authorization'] = `Bearer ${tokens.access_token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.setTokens(null);
      window.location.href = '/login';
      throw new Error('Oturum süresi doldu');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Bilinmeyen hata' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = params
      ? `${endpoint}?${new URLSearchParams(
          Object.entries(params)
            .filter(([, v]) => v !== undefined && v !== null)
            .map(([k, v]) => [k, String(v)])
        )}`
      : endpoint;
    return this.request<T>(url);
  }

  async post<T>(endpoint: string, body?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T>(endpoint: string, body: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete(endpoint: string): Promise<void> {
    await this.request<void>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
```

```typescript
// api/repositories.ts

import { apiClient } from './client';
import { Repository, PaginatedResponse } from '../types';

export const repositoryApi = {
  list: (params?: { page?: number; page_size?: number; search?: string }) =>
    apiClient.get<PaginatedResponse<Repository>>('/repositories', params),

  get: (id: string) =>
    apiClient.get<Repository>(`/repositories/${id}`),

  create: (data: { name: string; url: string; description?: string; default_branch?: string }) =>
    apiClient.post<Repository>('/repositories', data),

  update: (id: string, data: Partial<Repository>) =>
    apiClient.put<Repository>(`/repositories/${id}`, data),

  delete: (id: string) =>
    apiClient.delete(`/repositories/${id}`),

  clone: (id: string) =>
    apiClient.post(`/repositories/${id}/clone`),

  sync: (id: string) =>
    apiClient.post(`/repositories/${id}/sync`),
};
```

```typescript
// api/analyses.ts

import { apiClient } from './client';
import { Analysis, AnalysisResult, AnalysisConfig, PaginatedResponse } from '../types';

export const analysisApi = {
  list: (params?: { repo_id?: string; status?: string; page?: number; page_size?: number }) =>
    apiClient.get<PaginatedResponse<Analysis>>('/analyses', params),

  get: (id: string) =>
    apiClient.get<Analysis>(`/analyses/${id}`),

  create: (config: AnalysisConfig) =>
    apiClient.post<Analysis>('/analyses', config),

  getResult: (id: string) =>
    apiClient.get<AnalysisResult>(`/analyses/${id}/result`),

  delete: (id: string) =>
    apiClient.delete(`/analyses/${id}`),
};
```

```typescript
// api/commits.ts

import { apiClient } from './client';
import { Commit, CommitDetail, FileChange, PaginatedResponse } from '../types';

export const commitApi = {
  list: (params: {
    repo_id: string;
    page?: number;
    page_size?: number;
    author?: string;
    start_date?: string;
    end_date?: string;
  }) => apiClient.get<PaginatedResponse<Commit>>('/commits', params),

  get: (sha: string, repoId: string) =>
    apiClient.get<CommitDetail>(`/commits/${sha}`, { repo_id: repoId }),

  analyze: (sha: string, repoId: string, focusAreas?: string[]) =>
    apiClient.post(`/commits/${sha}/analyze`, undefined, {
      params: {
        repo_id: repoId,
        focus_areas: focusAreas,
      },
    }),

  explainChange: (sha: string, repoId: string, filePath: string) =>
    apiClient.get<{ explanation: string }>(`/commits/${sha}/explain`, {
      repo_id: repoId,
      file_path: filePath,
    }),
};
```

### 5.4 Sayfa Bileşenleri

```tsx
// pages/Dashboard.tsx

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { repositoryApi } from '../api/repositories';
import { analysisApi } from '../api/analyses';
import { Repository, Analysis } from '../types';

export function Dashboard() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [recentAnalyses, setRecentAnalyses] = useState<Analysis[]>([]);
  const [stats, setStats] = useState({
    totalRepos: 0,
    totalAnalyses: 0,
    completedAnalyses: 0,
    failedAnalyses: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  async function loadDashboardData() {
    try {
      setLoading(true);

      const [reposResponse, analysesResponse] = await Promise.all([
        repositoryApi.list({ page: 1, page_size: 5 }),
        analysisApi.list({ page: 1, page_size: 10 }),
      ]);

      setRepositories(reposResponse.items);
      setRecentAnalyses(analysesResponse.items);
      setStats({
        totalRepos: reposResponse.total,
        totalAnalyses: analysesResponse.total,
        completedAnalyses: analysesResponse.items.filter((a) => a.status === 'completed').length,
        failedAnalyses: analysesResponse.items.filter((a) => a.status === 'failed').length,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Veriler yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">Git depolarınızın genel durumu</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Toplam Depo"
          value={stats.totalRepos}
          icon="repository"
        />
        <StatCard
          title="Toplam Analiz"
          value={stats.totalAnalyses}
          icon="analysis"
        />
        <StatCard
          title="Tamamlanan"
          value={stats.completedAnalyses}
          icon="check"
        />
        <StatCard
          title="Başarısız"
          value={stats.failedAnalyses}
          icon="error"
        />
      </div>

      {/* Recent Repositories */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium text-gray-900">Son Eklenen Depolar</h2>
            <Link
              to="/repositories"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Tümünü Gör
            </Link>
          </div>
        </div>
        <div className="divide-y divide-gray-200">
          {repositories.map((repo) => (
            <Link
              key={repo.id}
              to={`/repositories/${repo.id}`}
              className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {repo.name}
                  </p>
                  <p className="text-sm text-gray-500 truncate">{repo.url}</p>
                </div>
                <div className="flex items-center space-x-2">
                  {repo.is_analyzed ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Analiz Edildi
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      Beklemede
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
          {repositories.length === 0 && (
            <div className="px-4 py-8 text-center text-gray-500">
              Henüz depo eklenmemiş.
            </div>
          )}
        </div>
      </div>

      {/* Recent Analyses */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium text-gray-900">Son Analizler</h2>
            <Link
              to="/analyses"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Tümünü Gör
            </Link>
          </div>
        </div>
        <div className="divide-y divide-gray-200">
          {recentAnalyses.map((analysis) => (
            <Link
              key={analysis.id}
              to={`/analyses/${analysis.id}`}
              className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">
                    Analiz #{analysis.id.slice(0, 8)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {analysis.processed_commits}/{analysis.total_commits} commit
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <StatusBadge status={analysis.status} />
                  {analysis.status === 'running' && (
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-indigo-600 h-2 rounded-full"
                        style={{ width: `${analysis.progress}%` }}
                      />
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))}
          {recentAnalyses.length === 0 && (
            <div className="px-4 py-8 text-center text-gray-500">
              Henüz analiz yapılmamış.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string; value: number; icon: string }) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-gray-100 rounded-md flex items-center justify-center">
              <span className="text-gray-600 text-sm">
                {icon === 'repository' && '📁'}
                {icon === 'analysis' && '🔍'}
                {icon === 'check' && '✓'}
                {icon === 'error' && '✗'}
              </span>
            </div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="text-lg font-semibold text-gray-900">{value}</dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const labels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}
    >
      {labels[status] || status}
    </span>
  );
}
```

```tsx
// pages/RepositoryDetail.tsx

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { repositoryApi } from '../api/repositories';
import { analysisApi } from '../api/analyses';
import { commitApi } from '../api/commits';
import { Repository, Analysis, Commit } from '../types';

export function RepositoryDetail() {
  const { id } = useParams<{ id: string }>();
  const [repository, setRepository] = useState<Repository | null>(null);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'commits' | 'analyses'>('overview');

  useEffect(() => {
    if (id) {
      loadRepositoryData(id);
    }
  }, [id]);

  async function loadRepositoryData(repoId: string) {
    try {
      setLoading(true);
      const [repo, analysesResp, commitsResp] = await Promise.all([
        repositoryApi.get(repoId),
        analysisApi.list({ repo_id: repoId, page: 1, page_size: 5 }),
        commitApi.list({ repo_id: repoId, page: 1, page_size: 20 }),
      ]);

      setRepository(repo);
      setAnalyses(analysesResp.items);
      setCommits(commitsResp.items);
    } catch (err) {
      console.error('Depo verileri yüklenirken hata:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!repository) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Depo bulunamadı</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              {repository.name}
            </h1>
            <p className="mt-1 text-sm text-gray-500">{repository.url}</p>
            {repository.description && (
              <p className="mt-2 text-sm text-gray-600">{repository.description}</p>
            )}
          </div>
          <div className="flex space-x-3">
            {!repository.local_path ? (
              <button
                onClick={() => handleClone(repository.id)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Klonla
              </button>
            ) : (
              <>
                <button
                  onClick={() => handleSync(repository.id)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Senkronize Et
                </button>
                <Link
                  to={`/analyses/new?repo=${repository.id}`}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Yeni Analiz Başlat
                </Link>
              </>
            )}
          </div>
        </div>

        {/* Metadata */}
        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div>
            <dt className="text-sm font-medium text-gray-500">Varsayılan Dal</dt>
            <dd className="mt-1 text-sm text-gray-900">{repository.default_branch}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Yerel Yol</dt>
            <dd className="mt-1 text-sm text-gray-900 truncate">
              {repository.local_path || 'Klonlanmamış'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Son Analiz</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {repository.last_analyzed_at
                ? new Date(repository.last_analyzed_at).toLocaleDateString('tr-TR')
                : 'Hiç'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Durum</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {repository.is_analyzed ? 'Analiz Edildi' : 'Analiz Edilmedi'}
            </dd>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {(['overview', 'commits', 'analyses'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab === 'overview' && 'Genel Bakış'}
              {tab === 'commits' && 'Commit\'ler'}
              {tab === 'analyses' && 'Analizler'}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Genel Bakış</h2>
          <p className="text-gray-600">
            Bu depo için detaylı analiz başlatmak için "Yeni Analiz Başlat" butonunu kullanın.
          </p>
        </div>
      )}

      {activeTab === 'commits' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Son Commit'ler</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {commits.map((commit) => (
              <Link
                key={commit.id}
                to={`/commits/${commit.sha}?repo=${repository.id}`}
                className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {commit.message}
                    </p>
                    <p className="text-sm text-gray-500">
                      {commit.author_name} · {new Date(commit.author_date).toLocaleDateString('tr-TR')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-green-600">+{commit.additions}</span>
                    <span className="text-red-600">-{commit.deletions}</span>
                    <span className="text-gray-500">{commit.files_changed} dosya</span>
                    <code className="text-gray-400">{commit.sha.slice(0, 7)}</code>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'analyses' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Analizler</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {analyses.map((analysis) => (
              <Link
                key={analysis.id}
                to={`/analyses/${analysis.id}`}
                className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Analiz #{analysis.id.slice(0, 8)}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysis.processed_commits}/{analysis.total_commits} commit
                    </p>
                  </div>
                  <StatusBadge status={analysis.status} />
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const labels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}

async function handleClone(repoId: string) {
  try {
    await repositoryApi.clone(repoId);
    window.location.reload();
  } catch (err) {
    console.error('Clone hatası:', err);
  }
}

async function handleSync(repoId: string) {
  try {
    await repositoryApi.sync(repoId);
    window.location.reload();
  } catch (err) {
    console.error('Sync hatası:', err);
  }
}
```

```tsx
// pages/AnalysisDetail.tsx

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { analysisApi } from '../api/analyses';
import { Analysis, AnalysisResult } from '../types';

export function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'summary' | 'insights' | 'files' | 'authors'>('summary');

  useEffect(() => {
    if (id) {
      loadAnalysis(id);
    }
  }, [id]);

  async function loadAnalysis(analysisId: string) {
    try {
      setLoading(true);
      const analysisData = await analysisApi.get(analysisId);
      setAnalysis(analysisData);

      if (analysisData.status === 'completed') {
        const resultData = await analysisApi.getResult(analysisId);
        setResult(resultData);
      }
    } catch (err) {
      console.error('Analiz verileri yüklenirken hata:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Analiz bulunamadı</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              Analiz #{analysis.id.slice(0, 8)}
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Başlangıç: {new Date(analysis.created_at).toLocaleString('tr-TR')}
            </p>
          </div>
          <StatusBadge status={analysis.status} />
        </div>

        {/* Progress */}
        {analysis.status === 'running' && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>
                {analysis.processed_commits}/{analysis.total_commits} commit işlendi
              </span>
              <span>%{analysis.progress.toFixed(1)}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${analysis.progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Error */}
        {analysis.error_message && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-800">{analysis.error_message}</p>
          </div>
        )}
      </div>

      {/* Results */}
      {analysis.status === 'completed' && result && (
        <>
          {/* Tabs */}
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {(['summary', 'insights', 'files', 'authors'] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab === 'summary' && 'Özet'}
                  {tab === 'insights' && 'İçgörüler'}
                  {tab === 'files' && 'Dosyalar'}
                  {tab === 'authors' && 'Yazarlar'}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          {activeTab === 'summary' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Özet</h2>
              <p className="text-gray-600 whitespace-pre-wrap">{result.summary}</p>

              <div className="mt-6 grid grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Toplam Commit</dt>
                  <dd className="mt-1 text-2xl font-semibold text-gray-900">
                    {result.statistics.total_commits}
                  </dd>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Eklenen Satır</dt>
                  <dd className="mt-1 text-2xl font-semibold text-green-600">
                    +{result.statistics.total_additions}
                  </dd>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Silinen Satır</dt>
                  <dd className="mt-1 text-2xl font-semibold text-red-600">
                    -{result.statistics.total_deletions}
                  </dd>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">İçgörüler</h2>
              <ul className="space-y-3">
                {result.insights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 text-sm font-medium">
                      {index + 1}
                    </span>
                    <p className="ml-3 text-gray-600">{insight}</p>
                  </li>
                ))}
              </ul>

              <h3 className="mt-6 text-lg font-medium text-gray-900 mb-4">Öneriler</h3>
              <ul className="space-y-2">
                {result.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 text-green-500 mr-2">•</span>
                    <p className="text-gray-600">{rec}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === 'files' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">En Çok Değişen Dosyalar</h2>
              <div className="space-y-2">
                {result.file_hotspots.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between py-2 border-b border-gray-100"
                  >
                    <code className="text-sm text-gray-900">{file.path}</code>
                    <span className="text-sm text-gray-500">{file.changes} değişiklik</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'authors' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Yazar Katkıları</h2>
              <div className="space-y-4">
                {result.author_contributions.map((author, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{author.name}</p>
                        <p className="text-sm text-gray-500">{author.commits} commit</p>
                      </div>
                      <div className="text-sm text-right">
                        <p className="text-green-600">+{author.additions}</p>
                        <p className="text-red-600">-{author.deletions}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const labels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}
```

```tsx
// pages/Commits.tsx

import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { commitApi } from '../api/commits';
import { Commit } from '../types';

export function Commits() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [commits, setCommits] = useState<Commit[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [authorFilter, setAuthorFilter] = useState('');

  const repoId = searchParams.get('repo') || '';

  useEffect(() => {
    if (repoId) {
      loadCommits();
    }
  }, [repoId, page, authorFilter]);

  async function loadCommits() {
    try {
      setLoading(true);
      const response = await commitApi.list({
        repo_id: repoId,
        page,
        page_size: 50,
        author: authorFilter || undefined,
      });
      setCommits(response.items);
      setTotal(response.total);
    } catch (err) {
      console.error('Commit\'ler yüklenirken hata:', err);
    } finally {
      setLoading(false);
    }
  }

  if (!repoId) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Lütfen bir depo seçin</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Commit'ler</h1>
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Yazar filtrele..."
            value={authorFilter}
            onChange={(e) => setAuthorFilter(e.target.value)}
            className="block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg">
          <div className="divide-y divide-gray-200">
            {commits.map((commit) => (
              <div
                key={commit.id}
                className="px-4 py-4 sm:px-6 hover:bg-gray-50"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {commit.message}
                    </p>
                    <p className="text-sm text-gray-500">
                      {commit.author_name} · {new Date(commit.author_date).toLocaleString('tr-TR')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-green-600">+{commit.additions}</span>
                    <span className="text-red-600">-{commit.deletions}</span>
                    <span className="text-gray-500">{commit.files_changed} dosya</span>
                    <code className="text-gray-400 font-mono">{commit.sha.slice(0, 7)}</code>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="px-4 py-3 border-t border-gray-200 sm:px-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-700">
                Toplam <span className="font-medium">{total}</span> commit
              </p>
              <div className="flex space-x-2">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Önceki
                </button>
                <span className="px-3 py-1 text-sm text-gray-700">
                  Sayfa {page}
                </span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={commits.length < 50}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Sonraki
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## 6. Rapor Oluşturucu

### 6.1 Rapor Servisi

```python
# services/report_service.py

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

        # Get relevant commits
        query = self.db.query(Commit).filter(Commit.repository_id == repository_id)

        if start_date:
            query = query.filter(Commit.author_date >= start_date)
        if end_date:
            query = query.filter(Commit.author_date <= end_date)

        commits = query.order_by(Commit.author_date.desc()).all()

        # Get file changes if specific files requested
        file_changes = []
        if file_paths:
            file_changes = self.db.query(FileChange).join(Commit).filter(
                Commit.repository_id == repository_id,
                FileChange.file_path.in_(file_paths),
            ).all()

        # Prepare analysis data
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
                for c in commits[:500]  # Limit for LLM context
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

        # Generate report content
        report_content = await self.llm.generate_report(analysis_data, report_type)

        # Convert to requested format
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
        """Detaylı bir dosya arkeoloji raporu oluşturur."""
        repo = self.db.query(Repository).filter(Repository.id == repository_id).first()
        if not repo:
            raise ValueError("Depo bulunamadı")

        # Get all changes for this file
        file_changes = self.db.query(FileChange).join(Commit).filter(
            Commit.repository_id == repository_id,
            FileChange.file_path == file_path,
        ).order_by(Commit.author_date).all()

        if not file_changes:
            return f"Bu dosya için değişiklik bulunamadı: {file_path}"

        # Build context for LLM
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
```

---

## 7. Veritabanı Migrasyonları

### 7.1 Alembic Yapısı

```python
# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.models import repository, user

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/gitarchaeology")
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

```sql
-- alembic/versions/001_initial.py

"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('avatar_url', sa.String(1024), nullable=True),
        sa.Column('oauth_provider', sa.String(50), nullable=True),
        sa.Column('oauth_id', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Repositories table
    op.create_table(
        'repositories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('url', sa.String(1024), nullable=False),
        sa.Column('local_path', sa.String(1024), nullable=True),
        sa.Column('default_branch', sa.String(255), server_default='main'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_analyzed', sa.Boolean, default=False),
        sa.Column('last_analyzed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now()),
        sa.Column('owner_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_index('ix_repositories_owner_id', 'repositories', ['owner_id'])
    op.create_index('ix_repositories_url', 'repositories', ['url'], unique=True)

    # Commits table
    op.create_table(
        'commits',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('repository_id', UUID(as_uuid=True), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('sha', sa.String(40), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('author_name', sa.String(255), nullable=False),
        sa.Column('author_email', sa.String(255), nullable=False),
        sa.Column('author_date', sa.DateTime, nullable=False),
        sa.Column('committer_name', sa.String(255), nullable=False),
        sa.Column('committer_email', sa.String(255), nullable=False),
        sa.Column('committer_date', sa.DateTime, nullable=False),
        sa.Column('parents', JSONB, nullable=True),
        sa.Column('additions', sa.Integer, default=0),
        sa.Column('deletions', sa.Integer, default=0),
        sa.Column('files_changed', sa.Integer, default=0),
        sa.Column('analyzed', sa.Boolean, default=False),
        sa.Column('analysis_result', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_commits_repository_id', 'commits', ['repository_id'])
    op.create_index('ix_commits_sha', 'commits', ['sha'])
    op.create_index('ix_commits_author_date', 'commits', ['author_date'])
    op.create_index('ix_commits_analyzed', 'commits', ['analyzed'])

    # File changes table
    op.create_table(
        'file_changes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('commit_id', UUID(as_uuid=True), sa.ForeignKey('commits.id'), nullable=False),
        sa.Column('file_path', sa.String(1024), nullable=False),
        sa.Column('old_path', sa.String(1024), nullable=True),
        sa.Column('change_type', sa.String(50), nullable=False),
        sa.Column('additions', sa.Integer, default=0),
        sa.Column('deletions', sa.Integer, default=0),
        sa.Column('diff', sa.Text, nullable=True),
        sa.Column('old_content', sa.Text, nullable=True),
        sa.Column('new_content', sa.Text, nullable=True),
        sa.Column('analysis', JSONB, nullable=True),
    )
    op.create_index('ix_file_changes_commit_id', 'file_changes', ['commit_id'])
    op.create_index('ix_file_changes_file_path', 'file_changes', ['file_path'])

    # Branches table
    op.create_table(
        'branches',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('repository_id', UUID(as_uuid=True), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('head_sha', sa.String(40), nullable=False),
        sa.Column('is_default', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_branches_repository_id', 'branches', ['repository_id'])

    # Analyses table
    op.create_table(
        'analyses',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('repository_id', UUID(as_uuid=True), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('status', sa.String(50), server_default='pending'),
        sa.Column('progress', sa.Float, default=0.0),
        sa.Column('total_commits', sa.Integer, default=0),
        sa.Column('processed_commits', sa.Integer, default=0),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('result', JSONB, nullable=True),
        sa.Column('config', JSONB, nullable=True),
        sa.Column('started_at', sa.DateTime, nullable=True),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_analyses_repository_id', 'analyses', ['repository_id'])
    op.create_index('ix_analyses_status', 'analyses', ['status'])

    # File snapshots table
    op.create_table(
        'file_snapshots',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('repository_id', UUID(as_uuid=True), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('file_path', sa.String(1024), nullable=False),
        sa.Column('commit_sha', sa.String(40), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('size_bytes', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_file_snapshots_repo_file', 'file_snapshots', ['repository_id', 'file_path'])
    op.create_index('ix_file_snapshots_content_hash', 'file_snapshots', ['content_hash'])


def downgrade() -> None:
    op.drop_table('file_snapshots')
    op.drop_table('analyses')
    op.drop_table('branches')
    op.drop_table('file_changes')
    op.drop_table('commits')
    op.drop_table('repositories')
    op.drop_table('users')
```

---

## 8. Docker Yapılandırması

### 8.1 Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/gitarchaeology
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4o
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-your-secret-key-change-in-production}
    volumes:
      - repo-data:/data/repos
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/gitarchaeology
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - repo-data:/data/repos
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: celery -A app.worker worker --loglevel=info --concurrency=4

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=gitarchaeology
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - redis-data:/data

volumes:
  pgdata:
  redis-data:
  repo-data:
```

### 8.2 Backend Dockerfile

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /data/repos

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.3 Frontend Dockerfile

```dockerfile
# frontend/Dockerfile

FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 8.4 Nginx Yapılandırması

```nginx
# frontend/nginx.conf

server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 9. Yapılandırma

### 9.1 Backend Yapılandırması

```python
# core/config.py

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Git Archaeology Tool"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/gitarchaeology"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    # Local LLM
    LOCAL_LLM_URL: str = "http://localhost:11434"
    LOCAL_LLM_MODEL: str = "llama3"

    # File Storage
    REPO_STORAGE_PATH: str = "/data/repos"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### 9.2 Backend Gereksinimleri

```txt
# backend/requirements.txt

fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
celery[redis]==5.3.6
gitpython==3.1.41
openai==1.12.0
anthropic==0.18.1
httpx==0.26.0
redis==5.0.1
markdown==3.5.2
python-dotenv==1.0.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

### 9.3 Frontend Paketleri

```json
{
  "name": "git-archaeology-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.1",
    "date-fns": "^3.3.1",
    "clsx": "^2.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@typescript-eslint/eslint-plugin": "^6.19.0",
    "@typescript-eslint/parser": "^6.19.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.12"
  }
}
```

---

## 10. Testler

### 10.1 Backend Testleri

```python
# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.main import app


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///./test.db")
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

```python
# tests/test_git_service.py

import pytest
from unittest.mock import MagicMock, patch
from app.services.git_service import GitService


class TestGitService:
    @pytest.fixture
    def git_service(self, tmp_path):
        # Create a minimal git repo for testing
        from git import Repo
        repo = Repo.init(tmp_path)
        return GitService(str(tmp_path))

    def test_validate_repo(self, git_service):
        assert git_service.validate_repo() is True

    def test_validate_repo_invalid(self, tmp_path):
        service = GitService(str(tmp_path / "nonexistent"))
        assert service.validate_repo() is False

    def test_get_repo_info(self, git_service):
        info = git_service.get_repo_info()
        assert "path" in info
        assert "branches" in info
        assert "head_sha" in info

    def test_get_commits_empty_repo(self, git_service):
        commits = git_service.get_commits()
        assert len(commits) == 0

    def test_get_file_changes_empty_repo(self, git_service):
        changes = git_service.get_file_changes("HEAD")
        assert len(changes) == 0
```

```python
# tests/test_analysis_engine.py

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.analysis_engine import AnalysisEngine
from app.services.git_service import GitService
from app.services.llm_service import LLMService


class TestAnalysisEngine:
    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def mock_git_service(self):
        return MagicMock(spec=GitService)

    @pytest.fixture
    def mock_llm_service(self):
        return MagicMock(spec=LLMService)

    @pytest.fixture
    def engine(self, mock_db, mock_git_service, mock_llm_service):
        return AnalysisEngine(mock_db, mock_git_service, mock_llm_service)

    def test_build_commit_analysis_prompt(self, engine):
        commit = MagicMock()
        commit.sha = "abc123"
        commit.message = "Test commit"
        commit.author_name = "Test User"
        commit.author_date = MagicMock()
        commit.author_date.isoformat.return_value = "2024-01-01T00:00:00"
        commit.additions = 10
        commit.deletions = 5
        commit.files_changed = 2

        prompt = engine._build_commit_analysis_prompt(commit, [])
        assert "Test commit" in prompt
        assert "abc123" in prompt
```

### 10.2 Frontend Testleri

```tsx
// src/__tests__/Dashboard.test.tsx

import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Dashboard } from '../pages/Dashboard';
import { apiClient } from '../api/client';

jest.mock('../api/client');

const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

describe('Dashboard', () => {
  beforeEach(() => {
    mockApiClient.get.mockReset();
  });

  it('renders loading state initially', () => {
    mockApiClient.get.mockResolvedValue({ items: [], total: 0, page: 1, page_size: 20 });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('renders dashboard data after loading', async () => {
    mockApiClient.get
      .mockResolvedValueOnce({ items: [{ id: '1', name: 'Test Repo' }], total: 1, page: 1, page_size: 5 })
      .mockResolvedValueOnce({ items: [], total: 0, page: 1, page_size: 10 });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Repo')).toBeInTheDocument();
    });
  });

  it('renders error state on failure', async () => {
    mockApiClient.get.mockRejectedValue(new Error('Network error'));

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/hata oluştu/)).toBeInTheDocument();
    });
  });
});
```

---

## 11. CI/CD

### 11.1 GitHub Actions

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run migrations
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          cd backend
          alembic upgrade head

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          cd backend
          pytest -v --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run lint
        run: |
          cd frontend
          npm run lint

      - name: Run type check
        run: |
          cd frontend
          npm run type-check

      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage

  docker-build:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]

    steps:
      - uses: actions/checkout@v4

      - name: Build backend
        run: docker build -t gitarchaeology-backend ./backend

      - name: Build frontend
        run: docker build -t gitarchaeology-frontend ./frontend
```

### 11.2 Docker Compose Development

```yaml
# docker-compose.dev.yml

version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - repo-data:/data/repos
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/gitarchaeology
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=true
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=gitarchaeology
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  pgdata:
  redis-data:
  repo-data:
```

```dockerfile
# backend/Dockerfile.dev

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-cov

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 12. Veri Akış Diyagramları

### 12.1 Analiz Akışı

```
Kullanıcı "Analiz Başlat" butonuna tıklar
         │
         ▼
Frontend: POST /api/v1/analyses
         │
         ▼
Backend: Analiz kaydı oluştur (status: pending)
         │
         ▼
Background task başlat
         │
         ▼
┌─────────────────────────────────────────┐
│  1. Git servisi ile commit'leri çek      │
│  2. Her batch için:                      │
│     a. Commit'u kaydet                   │
│     b. File change'leri kaydet           │
│     c. LLM ile analiz et                │
│     d. Sonucu kaydet                     │
│  3. İlerlemeyi güncelle                  │
└─────────────────────────────────────────┘
         │
         ▼
Tüm commit'ler işlendi
         │
         ▼
┌─────────────────────────────────────────┐
│  4. Genel özet oluştur (LLM)            │
│  5. Sonuçları analiz kaydına ekle        │
│  6. Durumu "completed" olarak güncelle    │
└─────────────────────────────────────────┘
         │
         ▼
Frontend: Polling ile durumu kontrol et
         │
         ▼
Sonuçları göster
```

### 12.2 Rapor Oluşturma Akışı

```
Kullanıcı rapor türünü seçer
         │
         ▼
Frontend: POST /api/v1/reports
         │
         ▼
Backend: İlgili commit ve file change'leri çek
         │
         ▼
Analiz verilerini hazırla
         │
         ▼
LLM ile rapor oluştur
         │
         ▼
┌─────────────────────────────────────────┐
│  Rapor türüne göre:                      │
│  - full: Kapsamlı rapor                  │
│  - summary: Kısa özet                    │
│  - security: Güvenlik odaklı             │
│  - architecture: Mimari analiz           │
│  - legacy: Legacy kod analizi            │
└─────────────────────────────────────────┘
         │
         ▼
Markdown formatında rapor dönüştür
         │
         ▼
İsteğe bağlı: HTML formatına çevir
         │
         ▼
Frontend: Raporu göster
```

---

## 13. Güvenlik

### 13.1 Kimlik Doğrulama

```python
# api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesap pasif",
        )

    return user
```

### 13.2 Rate Limiting

```python
# middleware/rate_limit.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client: redis.Redis):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        current = self.redis.get(key)
        if current and int(current) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail="Çok fazla istek. Lütfen bekleyin.",
            )

        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, 60)
        pipe.execute()

        response = await call_next(request)
        return response
```

---

## 14. Hata Yönetimi

```python
# middleware/error_handler.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            logger.error(f"beklenmeyen hata: {exc}")
            logger.error(traceback.format_exc())

            return JSONResponse(
                status_code=500,
                content={"detail": "Sunucu hatası oluştu"},
            )
```

---

## 15. Logger Yapılandırması

```python
# core/logging.py

import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO"):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log", encoding="utf-8"),
        ],
    )

    # Third-party library'lerin log seviyelerini ayarla
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("git").setLevel(logging.WARNING)
```

---

## 16. Proje Başlatma

### 16.1 Main Application

```python
# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.api.v1.routes import repository, analysis, commits, reports, auth

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Git depolarını analiz eden AI destekli araç",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlerMiddleware)

# Rotalar
app.include_router(auth.router, prefix="/api/v1")
app.include_router(repository.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(commits.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
```

### 16.2 Worker

```python
# worker.py

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "gitarchaeology",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    worker_max_tasks_per_child=100,
)
```

### 16.3 .env Örneği

```env
# .env

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gitarchaeology

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4o

# Anthropic (opsiyonel)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Local LLM (opsiyonel)
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3

# App
DEBUG=true
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

---

## 17. CLI Arayüzü (Opsiyonel)

```python
# cli/main.py

import click
import asyncio
from pathlib import Path

from app.services.git_service import GitService
from app.services.analysis_engine import AnalysisEngine
from app.services.llm_service import LLMService
from app.database import SessionLocal


@click.group()
def cli():
    """Git Arkeoloji Aracı - CLI"""
    pass


@cli.command()
@click.argument("repo_path")
def info(repo_path: str):
    """Depo hakkında bilgi göster."""
    git_service = GitService(repo_path)
    if not git_service.validate_repo():
        click.echo("Geçersiz Git deposu", err=True)
        return

    info = git_service.get_repo_info()
    click.echo(f"Yol: {info['path']}")
    click.echo(f"Dallar: {', '.join(info['branches'])}")
    click.echo(f"Aktif Dal: {info['current_branch']}")
    click.echo(f"HEAD: {info['head_sha'][:8]}")
    click.echo(f"Uzak URL: {info['remote_url']}")


@cli.command()
@click.argument("repo_path")
@click.option("--max-count", "-n", default=50, help="Gösterilecek commit sayısı")
def log(repo_path: str, max_count: int):
    """Son commit'leri göster."""
    git_service = GitService(repo_path)
    commits = git_service.get_commits(max_count=max_count)

    for commit in commits:
        click.echo(f"{commit.sha[:8]} | {commit.author_date.strftime('%Y-%m-%d')} | {commit.author_name:<20} | {commit.message[:60]}")


@cli.command()
@click.argument("repo_path")
@click.argument("sha")
def show(sha: str, repo_path: str):
    """Commit detayını göster."""
    git_service = GitService(repo_path)
    changes = git_service.get_file_changes(sha)

    for change in changes:
        color = "green" if change.change_type == "added" else "red" if change.change_type == "deleted" else "yellow"
        click.echo(click.style(f"{change.change_type:10} {change.file_path}", fg=color))
        click.echo(f"           +{change.additions} -{change.deletions}")


@cli.command()
@click.argument("repo_path")
@click.option("--llm-provider", default="openai", help="LLM provider")
def analyze(repo_path: str, llm_provider: str):
    """Depoyu analiz et."""
    db = SessionLocal()
    try:
        git_service = GitService(repo_path)
        llm_service = LLMService(provider=llm_provider)
        engine = AnalysisEngine(db, git_service, llm_service)

        # Basit analiz
        commits = git_service.get_commits(max_count=100)
        click.echo(f"{len(commits)} commit analiz ediliyor...")

        for i, commit in enumerate(commits, 1):
            click.echo(f"[{i}/{len(commits)}] {commit.sha[:8]} - {commit.message[:50]}")
    finally:
        db.close()


if __name__ == "__main__":
    cli()
```

---

## 18. Dokümantasyon Yapısı

```
docs/
├── api/
│   ├── repositories.md
│   ├── analyses.md
│   ├── commits.md
│   └── reports.md
├── architecture/
│   ├── overview.md
│   ├── database.md
│   └── security.md
├── deployment/
│   ├── docker.md
│   ├── kubernetes.md
│   └── environment.md
├── development/
│   ├── setup.md
│   ├── testing.md
│   └── contributing.md
└── user-guide/
    ├── getting-started.md
    ├── creating-repository.md
    ├── running-analysis.md
    └── generating-reports.md
```

---

## 19. Performans Optimizasyonları

### 19.1 Veritabanı İndeksleri

```sql
-- Composite indexes for common queries
CREATE INDEX idx_commits_repo_date ON commits(repository_id, author_date DESC);
CREATE INDEX idx_commits_repo_author ON commits(repository_id, author_name);
CREATE INDEX idx_file_changes_repo_path ON file_changes(commit_id, file_path);
CREATE INDEX idx_analyses_repo_status ON analyses(repository_id, status);

-- Partial indexes
CREATE INDEX idx_commits_unanalyzed ON commits(repository_id)
WHERE analyzed = false;

CREATE INDEX idx_analyses_running ON analyses(repository_id)
WHERE status = 'running';
```

### 19.2 Cache Stratejisi

```python
# services/cache_service.py

import json
import redis
from typing import Optional, Any
from functools import wraps

from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
        self.default_ttl = 3600  # 1 hour

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, ttl: int = None):
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value, default=str),
        )

    def delete(self, key: str):
        self.redis.delete(key)

    def invalidate_pattern(self, pattern: str):
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)


def cache_result(key_prefix: str, ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = CacheService()
            cache_key = f"{key_prefix}:{hash(str(args) + str(kwargs))}"

            cached = cache.get(cache_key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
```

---

## 20. Monitoring ve Observability

```python
# middleware/monitoring.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.3f}s"
        )

        response.headers["X-Process-Time"] = str(duration)

        return response
```

---

## 21. Uluslararasılaştırma (i18n)

```python
# core/i18n.py

from typing import Dict, Any
import json
from pathlib import Path


class I18n:
    def __init__(self, locale: str = "tr"):
        self.locale = locale
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Any]:
        trans_file = Path(f"locales/{self.locale}.json")
        if trans_file.exists():
            return json.loads(trans_file.read_text(encoding="utf-8"))
        return {}

    def t(self, key: str, **kwargs) -> str:
        value = self.translations.get(key, key)
        if kwargs:
            value = value.format(**kwargs)
        return value


# locales/tr.json
{
    "analysis": {
        "started": "Analiz başlatıldı: {repo_name}",
        "completed": "Analiz tamamlandı: {repo_name}",
        "failed": "Analiz başarısız: {error}",
        "progress": "İlerleme: {progress}%"
    },
    "report": {
        "generated": "Rapor oluşturuldu: {report_type}",
        "download": "Raporu indir"
    },
    "errors": {
        "not_found": "Bulunamadı",
        "unauthorized": "Yetkisiz erişim",
        "server_error": "Sunucu hatası"
    }
}
```

---

## 22. Proje Dosya Yapısı Özeti

```
git-archaeology/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       └── routes/
│   │   │           ├── analysis.py
│   │   │           ├── auth.py
│   │   │           ├── commits.py
│   │   │           ├── reports.py
│   │   │           └── repository.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── i18n.py
│   │   │   └── logging.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── middleware/
│   │   │   ├── error_handler.py
│   │   │   ├── monitoring.py
│   │   │   └── rate_limit.py
│   │   ├── models/
│   │   │   ├── repository.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   └── repository.py
│   │   └── services/
│   │       ├── analysis_engine.py
│   │       ├── cache_service.py
│   │       ├── git_service.py
│   │       ├── llm_service.py
│   │       └── report_service.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_analysis_engine.py
│   │   └── test_git_service.py
│   ├── cli/
│   │   └── main.py
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   ├── analyses.ts
│   │   │   ├── client.ts
│   │   │   ├── commits.ts
│   │   │   ├── repositories.ts
│   │   │   └── reports.ts
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── analysis/
│   │   │   ├── commits/
│   │   │   ├── repositories/
│   │   │   └── reports/
│   │   ├── hooks/
│   │   ├── pages/
│   │   │   ├── Analysis.tsx
│   │   │   ├── AnalysisDetail.tsx
│   │   │   ├── Commits.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Repositories.tsx
│   │   │   ├── RepositoryDetail.tsx
│   │   │   ├── Reports.tsx
│   │   │   └── Settings.tsx
│   │   ├── store/
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── deployment/
│   ├── development/
│   └── user-guide/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env.example
├── .gitignore
├── README.md
└── PROMPT.md
```

---

## 23. Çıkış Kontrol Listesi

- [ ] Backend API tamamlandı
- [ ] Frontend UI tamamlandı
- [ ] Veritabanı migrasyonları hazır
- [ ] Docker yapılandırması hazır
- [ ] Testler yazıldı
- [ ] CI/CD pipeline kuruldu
- [ ] Dokümantasyon yazıldı
- [ ] Security audit yapıldı
- [ ] Performance testleri yapıldı
- [ ] Uygulama deploy edildi

---

## 24. Gelecek Özellikler (Roadmap)

### Faz 2
- [ ] GitHub/GitLab OAuth entegrasyonu
- [ ] Çoklu depo analizi
- [ ] Özel LLM modelleri desteği
- [ ] Rapor dışa aktarma (PDF, Excel)
- [ ] WebSocket ile real-time güncelleme

### Faz 3
- [ ] CI/CD pipeline entegrasyonu
- [ ] Slack/Teams bildirimleri
- [ ] API versioning
- [ ] Webhook desteği
- [ ] Plugin sistemi

### Faz 4
- [ ] Enterprise özellikleri
- [ ] SSO/LDAP entegrasyonu
- [ ] Audit log
- [ ] Multi-tenant yapı
- [ ] SLA monitoring

---

## 25. Katkıda Bulunma Rehberi

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları
- Python: PEP 8, black formatting
- TypeScript: ESLint + Prettier
- Commit mesajları: Conventional Commits formatı
- Branch isimleri: `feature/`, `bugfix/`, `hotfix/` prefix

---

**Son Güncelleme:** 2024
**Versiyon:** 1.0.0
**Lisans:** MIT
