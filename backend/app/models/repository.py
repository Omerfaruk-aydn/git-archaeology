from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    Boolean, Float, JSON, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    local_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    default_branch: Mapped[str] = mapped_column(String(255), default="main")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_analyzed: Mapped[bool] = mapped_column(Boolean, default=False)
    last_analyzed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="repositories")
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

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_id: Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id"))
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
    analysis_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

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

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    commit_id: Mapped[str] = mapped_column(String(36), ForeignKey("commits.id"))
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    old_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False)
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    diff: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    old_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    analysis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    commit: Mapped["Commit"] = relationship(back_populates="file_changes")

    __table_args__ = (
        Index("ix_file_changes_commit_id", "commit_id"),
        Index("ix_file_changes_file_path", "file_path"),
    )


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_id: Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    head_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    repository: Mapped["Repository"] = relationship(back_populates="branches")

    __table_args__ = (
        Index("ix_branches_repository_id", "repository_id"),
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_id: Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    total_commits: Mapped[int] = mapped_column(Integer, default=0)
    processed_commits: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    repository: Mapped["Repository"] = relationship(back_populates="analyses")

    __table_args__ = (
        Index("ix_analyses_repository_id", "repository_id"),
        Index("ix_analyses_status", "status"),
    )


class FileSnapshot(Base):
    __tablename__ = "file_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_id: Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id"))
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    repository: Mapped["Repository"] = relationship(back_populates="file_snapshots")

    __table_args__ = (
        Index("ix_file_snapshots_repo_file", "repository_id", "file_path"),
        Index("ix_file_snapshots_content_hash", "content_hash"),
    )
