from django.apps import AppConfig


class RasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ras'

    def ready(self) -> None:
        from .models import AuditUpload
        from vectordb.shortcuts import autosync_model_to_vectordb
        autosync_model_to_vectordb(AuditUpload)
