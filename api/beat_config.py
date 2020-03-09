from celery.schedules import crontab

DEFAULT_OPTIONS = {
    # ensure we don't accumulate a huge backlog of these if the workers are down
    'expires': 30
}


CELERYBEAT_SCHEDULE = {
    'Dummy task - can be removed': {
        'task': 'bookshelf.core.tasks.check_django',
        'schedule': crontab(minute='0', hour='0', day_of_week='*', day_of_month='1', month_of_year='1'),  # 1Jan yearly
        'options': DEFAULT_OPTIONS,
    },
}
