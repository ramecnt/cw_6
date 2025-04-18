import os

from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            from mailing.services import start
            start()
