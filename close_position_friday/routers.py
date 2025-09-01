class QueueDBRouter:
    app_label = "django_q"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "queue_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return "queue_db"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return db == "queue_db"
        return None
