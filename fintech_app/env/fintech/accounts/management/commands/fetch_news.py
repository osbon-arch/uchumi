# accounts/management/commands/fetch_news.py

from django.core.management.base import BaseCommand
from accounts.utils import fetch_latest_finance_news

class Command(BaseCommand):
    help = 'Fetch latest finance news'

    def handle(self, *args, **kwargs):
        fetch_latest_finance_news()
        self.stdout.write(self.style.SUCCESS('Successfully fetched latest finance news!'))
