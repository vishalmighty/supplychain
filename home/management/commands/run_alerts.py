from django.core.management.base import BaseCommand
from home.alerts import check_inventory

class Command(BaseCommand):
    help = 'Runs my custom cron job'

    def handle(self, *args, **options):
        check_inventory()
