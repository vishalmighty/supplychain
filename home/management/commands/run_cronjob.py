from django.core.management.base import BaseCommand
from home.csv_work import my_cron_job

class Command(BaseCommand):
    help = 'Runs my custom cron job'

    def handle(self, *args, **options):
        my_cron_job()
