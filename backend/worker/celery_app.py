from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-feeds-every-15-minutes": {
        "task": "worker.tasks.schedule_feed_fetches",
        "schedule": crontab(minute="*/15"),
    },
}
