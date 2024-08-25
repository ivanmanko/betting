from celery import Celery
import tasks  
from config import settings

celery_app = Celery(
    "app",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
)

celery_app.conf.task_routes = {
    'tasks.run_check_events_deadline': {'queue': 'celery'},
}


# Добавляем расписание для задач
celery_app.conf.beat_schedule = {
    'check-events-deadline-every-30-seconds': {
        'task': 'tasks.run_check_events_deadline',  
        'schedule': 30.0,  
        'args': ()  
    },
}

# Импортируем и регистрируем задачи
celery_app.autodiscover_tasks(['tasks'])

if __name__ == '__main__':
    celery_app.start()
