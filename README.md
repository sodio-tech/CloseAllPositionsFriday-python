# DjangoQ task schedule- Close All position on Friday

## Setup Instructions

### 1. Commands


DjangoQ task schedule

# Schedule task to run at a specific time

python manage.py schedule_friday_task --day friday --time 21:55 --force

#migrate command

python manage.py migrate --database=queue_db

# run task server

python manage.py qcluster


### 2. Troubleshooting

If the worker is not processing tasks:

- Make sure Redis is running and accessible
- Check that both worker and beat are running
- Verify the worker is consuming from the right queue
- Check logs for any errors

### 3. Changing the Schedule

To change the schedule, update the environment variables in your `.env` file:

```
# Schedule task (24-hour format)
TASK_SCHEDULE_HOUR=5    # Change to desired hour (0-23)
TASK_SCHEDULE_MINUTE=0  # Change to desired minute (0-59)
```

### 4. Files to Watch

- `background_tasks/tasks.py`
- `background_tasks/view.py`
- `core/__init__.py`
- `core/celery.py`
- `core/settings.py`
- `core/urls.py`
- `.env.example`
- `.gitignore`
