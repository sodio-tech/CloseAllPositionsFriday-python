import os
import dotenv

dotenv.load_dotenv()

from celery import Celery
from celery.schedules import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Configure Celery for Windows
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_retry = True
app.conf.worker_pool = "solo"
app.conf.timezone = "UTC"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Get interval settings from environment variables
interval = int(os.getenv("TASK_SCHEDULE_INTERVAL", 1))
interval_unit = os.getenv("TASK_SCHEDULE_INTERVAL_UNIT", "minutes")

# Create interval kwargs using the unit directly as the key
interval_kwargs = {interval_unit: interval}
app.conf.broker_transport_options = {"global_keyprefix": "equity_historization"}
# Define the beat schedule
app.conf.beat_schedule = {
    "equity_historization": {
        "task": "background_task.tasks.equity_historization",
        "schedule": timedelta(**interval_kwargs),
    },
}
