import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from background_task.tasks import equity_historization


def debug_background_task():

    equity_historization()


if __name__ == "__main__":
    debug_background_task()
