"""SQLite compatible migration

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    dialect = conn.dialect.name

    if dialect == 'sqlite':
        op.drop_table('file_snapshots')
        op.drop_table('analyses')
        op.drop_table('branches')
        op.drop_table('file_changes')
        op.drop_table('commits')
        op.drop_table('repositories')
        op.drop_table('users')

    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
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

    op.create_table(
        'repositories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('url', sa.String(1024), nullable=False),
        sa.Column('local_path', sa.String(1024), nullable=True),
        sa.Column('default_branch', sa.String(255), server_default='main'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_analyzed', sa.Boolean, default=False),
        sa.Column('last_analyzed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now()),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_index('ix_repositories_owner_id', 'repositories', ['owner_id'])
    op.create_index('ix_repositories_url', 'repositories', ['url'], unique=True)

    op.create_table(
        'commits',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('repository_id', sa.String(36), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('sha', sa.String(40), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('author_name', sa.String(255), nullable=False),
        sa.Column('author_email', sa.String(255), nullable=False),
        sa.Column('author_date', sa.DateTime, nullable=False),
        sa.Column('committer_name', sa.String(255), nullable=False),
        sa.Column('committer_email', sa.String(255), nullable=False),
        sa.Column('committer_date', sa.DateTime, nullable=False),
        sa.Column('parents', sa.JSON, nullable=True),
        sa.Column('additions', sa.Integer, default=0),
        sa.Column('deletions', sa.Integer, default=0),
        sa.Column('files_changed', sa.Integer, default=0),
        sa.Column('analyzed', sa.Boolean, default=False),
        sa.Column('analysis_result', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_commits_repository_id', 'commits', ['repository_id'])
    op.create_index('ix_commits_sha', 'commits', ['sha'])
    op.create_index('ix_commits_author_date', 'commits', ['author_date'])
    op.create_index('ix_commits_analyzed', 'commits', ['analyzed'])

    op.create_table(
        'file_changes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('commit_id', sa.String(36), sa.ForeignKey('commits.id'), nullable=False),
        sa.Column('file_path', sa.String(1024), nullable=False),
        sa.Column('old_path', sa.String(1024), nullable=True),
        sa.Column('change_type', sa.String(50), nullable=False),
        sa.Column('additions', sa.Integer, default=0),
        sa.Column('deletions', sa.Integer, default=0),
        sa.Column('diff', sa.Text, nullable=True),
        sa.Column('old_content', sa.Text, nullable=True),
        sa.Column('new_content', sa.Text, nullable=True),
        sa.Column('analysis', sa.JSON, nullable=True),
    )
    op.create_index('ix_file_changes_commit_id', 'file_changes', ['commit_id'])
    op.create_index('ix_file_changes_file_path', 'file_changes', ['file_path'])

    op.create_table(
        'branches',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('repository_id', sa.String(36), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('head_sha', sa.String(40), nullable=False),
        sa.Column('is_default', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_branches_repository_id', 'branches', ['repository_id'])

    op.create_table(
        'analyses',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('repository_id', sa.String(36), sa.ForeignKey('repositories.id'), nullable=False),
        sa.Column('status', sa.String(50), server_default='pending'),
        sa.Column('progress', sa.Float, default=0.0),
        sa.Column('total_commits', sa.Integer, default=0),
        sa.Column('processed_commits', sa.Integer, default=0),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('result', sa.JSON, nullable=True),
        sa.Column('config', sa.JSON, nullable=True),
        sa.Column('started_at', sa.DateTime, nullable=True),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )
    op.create_index('ix_analyses_repository_id', 'analyses', ['repository_id'])
    op.create_index('ix_analyses_status', 'analyses', ['status'])

    op.create_table(
        'file_snapshots',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('repository_id', sa.String(36), sa.ForeignKey('repositories.id'), nullable=False),
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
