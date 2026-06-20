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

        commits = git_service.get_commits(max_count=100)
        click.echo(f"{len(commits)} commit analiz ediliyor...")

        for i, commit in enumerate(commits, 1):
            click.echo(f"[{i}/{len(commits)}] {commit.sha[:8]} - {commit.message[:50]}")
    finally:
        db.close()


if __name__ == "__main__":
    cli()
