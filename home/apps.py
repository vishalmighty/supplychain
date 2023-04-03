from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    def ready(self):
        # import the Python file you want to run
        from .alerts import check_inventory

        # call the function that runs your code
