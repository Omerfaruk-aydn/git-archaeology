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
