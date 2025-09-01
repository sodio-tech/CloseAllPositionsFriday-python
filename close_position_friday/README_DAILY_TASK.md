# close position on friday Task

This document explains how the daily EOD (End of Day) equity report task is configured and managed.

## Overview

The daily task is configured to run automatically at midnight (00:00) every day using Django-Q2. The task is responsible for generating daily equity reports and processing end-of-day data.

## Configuration

### Task Function

- **Location**: `close_position_friday/tasks/daily_report_task.py`
- **Function**: `daily_report_task()`
- **Full Path**: `close_position_friday.tasks.daily_report_task.daily_report_task`
- **Schedule**: Daily at midnight (00:00)

### Django-Q Configuration

The task uses Django-Q2 for scheduling with the following configuration in `core/settings.py`:

```python
Q_CLUSTER = {
    "name": "QueueCluster",
    "workers": 4,
    "timeout": 60,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "queue_db",  # Uses separate SQLite database
}
```

### Database Configuration

The Django-Q schedules are stored in a separate SQLite database (`queue_db.sqlite3`) to avoid conflicts with the main PostgreSQL database.

## Management Commands

### Schedule the Daily Task

```bash
# Schedule task to run at midnight (default)
python manage.py schedule_daily_task

# Schedule task to run at a specific time
python manage.py schedule_daily_task --time 23:30 --force

# Force recreate the schedule
python manage.py schedule_daily_task --force
```

### Check Existing Schedules

```bash
python manage.py shell -c "from django_q.models import Schedule; [print(f'ID: {s.id}, Func: {s.func}, Next run: {s.next_run}') for s in Schedule.objects.all()]"
```

## Running the QCluster

To process scheduled tasks, you need to run the Django-Q cluster:

```bash
# Run the cluster (recommended for production)
python manage.py qcluster

# Run once and exit (for testing)
python manage.py qcluster --run-once
```

## Troubleshooting

### Task Not Running

1. **Check if QCluster is running**: Ensure `python manage.py qcluster` is running
2. **Verify schedule exists**: Use the management command to check schedules
3. **Check timezone**: Ensure your server timezone matches the expected timezone
4. **Check logs**: Look for any error messages in the QCluster output

### Schedule Not Created

1. **Check app configuration**: Ensure `eod_equity_monitor` is in `INSTALLED_APPS`
2. **Run migrations**: Ensure Django-Q tables are created
3. **Manual scheduling**: Use the management command to manually create the schedule

### Task Not Executing

1. **Check function path**: Ensure the task uses the full path `eod_equity_monitor.tasks.daily_report_task.daily_report_task`
2. **Check import structure**: Ensure the task is properly imported in `eod_equity_monitor/tasks/__init__.py`
3. **Test manually**: Try running the task manually to ensure it works

### Timezone Issues

The task uses the timezone configured in Django settings (`TIME_ZONE = "UTC"`). If you need a different timezone:

1. Update `TIME_ZONE` in `core/settings.py`
2. Recreate the schedule using the management command

## Development

### Testing the Task

```bash
# Test the task function directly
python manage.py shell -c "from eod_equity_monitor.tasks.daily_report_task import daily_report_task; daily_report_task()"

# Test with QCluster
python manage.py qcluster --run-once
```

### Adding Task Logic

Edit `eod_equity_monitor/tasks/daily_report_task.py` to add your daily processing logic:

```python
def daily_report_task():
    """Daily report generation task that runs at midnight"""
    current_time = timezone.now()
    logger.info(f"Daily report task executed at: {current_time}")

    # Add your daily report logic here
    # - Generate EOD equity reports
    # - Process daily statistics
    # - Send notifications

    return f"Daily report completed at {current_time}"
```

## Production Deployment

### Systemd Service (Recommended)

Create a systemd service to run the QCluster:

```ini
[Unit]
Description=Django Q Cluster
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/python manage.py qcluster
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Cron Alternative

If you prefer using system cron instead of Django-Q:

```bash
# Add to crontab (runs at midnight)
0 0 * * * cd /path/to/your/project && /path/to/your/venv/bin/python manage.py shell -c "from eod_equity_monitor.tasks.daily_report_task import daily_report_task; daily_report_task()"
```

## Monitoring

### Check Task Status

```bash
# Check recent task results
python manage.py shell -c "from django_q.models import Success; [print(f'Task: {s.func}, Started: {s.started}, Duration: {s.duration}') for s in Success.objects.order_by('-started')[:5]]"
```

### Logs

The task logs to both:

- Django logging system (configured in settings)
- Console output (when running manually)

## Files Modified

1. `close_position_friday/apps.py` - Auto-scheduling configuration
2. `close_position_friday/tasks/close_position_task.py` - Task function
3. `close_position_friday/management/commands/schedule_friday_task.py` - Management command
4. `core/settings.py` - Django-Q configuration
5. `close_position_friday/routers.py` - Database routing for Django-Q
