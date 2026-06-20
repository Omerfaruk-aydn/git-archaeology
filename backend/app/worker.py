from app.core.config import settings

try:
    from celery import Celery
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
except Exception:
    celery_app = None
