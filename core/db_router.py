class CeleryBeatRouter:
    """
    Route database operations for the django_celery_beat app to the celery_beat database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "django_celery_beat":
            return "celery_beat"

        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "django_celery_beat":
            return "celery_beat"

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both objects are in the same database
        db_set = {obj1._state.db, obj2._state.db}

        return len(db_set) == 1

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "django_celery_beat":
            return db == "celery_beat"

        return db == "default"
