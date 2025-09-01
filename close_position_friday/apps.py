import sys
import threading

from django.apps import AppConfig


class ClosePositionFridayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "close_position_friday"

    def ready(self):
        if any(
            cmd in sys.argv
            for cmd in ["makemigrations", "migrate", "collectstatic", "shell"]
        ):
            return

        def schedule_task():
            from django_q.models import Schedule
            from django_q.tasks import schedule
            from django.utils import timezone
            from datetime import timedelta

            # Get current UTC time
            now = timezone.now()

            # Calculate next Friday at 21:55 UTC
            days_until_friday = (4 - now.weekday()) % 7  # 4 = Friday (0=Monday, 6=Sunday)
            if days_until_friday == 0 and now.hour >= 21 and now.minute >= 55:
                # If it's already Friday after 21:55, schedule for next Friday
                days_until_friday = 7
            
            next_friday = now + timedelta(days=days_until_friday)
            next_run_time = next_friday.replace(hour=21, minute=55, second=0, microsecond=0)

            task_name = "close_position_friday.tasks.close_position_task.close_position_task"

            if not Schedule.objects.filter(func=task_name).exists():
                schedule(
                    task_name,
                    schedule_type=Schedule.WEEKLY,
                    repeats=-1,
                    next_run=next_run_time,
                )
                print(f"Scheduled weekly Friday task '{task_name}' to run at {next_run_time} UTC")
            else:
                print(f"Task '{task_name}' already scheduled")

        # Delay to allow app to finish initializing
        threading.Timer(5, schedule_task).start()
