from django.apps import AppConfig


class CoinsConfig(AppConfig):
    name = 'coins'

    def ready(self):
        from coins_updater import update
        update.start()
