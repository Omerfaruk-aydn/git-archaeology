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
