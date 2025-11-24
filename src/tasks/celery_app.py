from celery import Celery
from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"],
)

# celery_instance.conf.beat_schedule = {
#     "tag":{
#         "task": "booking_today_check_in",
#         "schedule": 10
#     }
# }