from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'api.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import api.authentication.signals


default_app_config = 'api.authentication.AuthenticationConfig'
