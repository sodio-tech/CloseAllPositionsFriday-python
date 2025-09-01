from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Schedule the weekly Friday close position task at 21:55 UTC"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force recreate the schedule even if it exists",
        )
        parser.add_argument(
            "--time",
            type=str,
            default="21:55",
            help="Time to run the task (HH:MM format, default: 21:55)",
        )
        parser.add_argument(
            "--day",
            type=str,
            choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            default="friday",
            help="Day of the week to run the task (default: friday)",
        )

    def handle(self, *args, **options):
        force = options["force"]
        time_str = options["time"]
        day_str = options["day"]

        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time format")
        except ValueError:
            self.stdout.write(
                self.style.ERROR(f"Invalid time format: {time_str}. Use HH:MM format.")
            )
            return

        # Convert day string to weekday number (0=Monday, 6=Sunday)
        day_mapping = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        target_weekday = day_mapping[day_str.lower()]

        task_name = "close_position_friday.tasks.close_position_task.close_position_task"

        # Check if schedule already exists
        existing_schedule = Schedule.objects.filter(func=task_name).first()

        if existing_schedule and not force:
            self.stdout.write(
                self.style.WARNING(
                    f'Task "{task_name}" is already scheduled to run at {existing_schedule.next_run}'
                )
            )
            return

        # Delete existing schedule if force is True
        if existing_schedule and force:
            existing_schedule.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Deleted existing schedule for "{task_name}"')
            )

        # Get current local time
        now = timezone.now()

        # Calculate next target day at specified time
        days_until_target = (target_weekday - now.weekday()) % 7
        if days_until_target == 0 and now.hour >= hour and now.minute >= minute:
            # If it's already the target day after the specified time, schedule for next week
            days_until_target = 7
        
        next_target_day = now + timedelta(days=days_until_target)
        next_run_time = next_target_day.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # Create new schedule for weekly Friday execution
        schedule(
            task_name,
            schedule_type=Schedule.WEEKLY,
            repeats=-1,
            next_run=next_run_time,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Scheduled weekly {day_str.capitalize()} task "{task_name}" to run at {next_run_time.strftime("%Y-%m-%d %H:%M:%S")} UTC'
            )
        )

        # Show all schedules
        schedules = Schedule.objects.filter(func=task_name)
        self.stdout.write("\nCurrent schedules:")
        for s in schedules:
            self.stdout.write(
                f"  ID: {s.id}, Next run: {s.next_run}, Repeats: {s.repeats}"
            )
