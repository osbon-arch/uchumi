# accounts/tasks.py

from celery import shared_task
from .utils import fetch_latest_finance_news

@shared_task
def fetch_finance_news_task():
    fetch_latest_finance_news()
