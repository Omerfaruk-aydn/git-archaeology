import pytest
from unittest.mock import MagicMock, patch
from app.services.git_service import GitService


class TestGitService:
    @pytest.fixture
    def git_service(self, tmp_path):
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
