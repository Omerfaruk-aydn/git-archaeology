from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict
import uuid


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


class AnalysisCreate(BaseModel):
    repository_id: uuid.UUID
    branch: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_commits: Optional[int] = Field(None, ge=1, le=100000)
    llm_provider: str = Field(default="openai", pattern="^(openai|anthropic|local|openrouter|azure|bedrock|gemini|groq|together|mistral|cohere|deepseek|xai|fireworks|huggingface|replicate|baidu|dashscope|moonshot|zhipuai|minimax|deepinfra|perplexity|cloudflare)$")
    llm_model: str = Field(default="gpt-4o")
    focus_areas: Optional[List[str]] = None
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
    insights: List[Any]
    recommendations: List[str]


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


CommitDetailResponse.model_rebuild()
