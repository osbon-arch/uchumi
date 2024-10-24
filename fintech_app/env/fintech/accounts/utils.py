# accounts/utils.py

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64



#web scraping
# accounts/utils.py


from bs4 import BeautifulSoup
from .models import NewsArticle


def fetch_latest_finance_news():
    url = 'https://www.example-finance-news-site.com/'  # Replace with the actual news site
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')  # Adjust this based on the site's HTML structure
        
        for article in articles:
            title = article.find('h2').get_text()  # Adjust based on the site's HTML structure
            link = article.find('a')['href']  # Adjust based on the site's HTML structure
            published_at = datetime.now()  # Or parse the published date if available
            
            # Save or update the article in the database
            NewsArticle.objects.update_or_create(
                title=title,
                defaults={'url': link, 'published_at': published_at}
            )


def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
    
def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_mpesa_access_token()
    if not access_token:
        return None

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((settings.MPESA_LIPA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": settings.MPESA_LIPA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 254758350608,  # Customer phone number in 254 format
        "PartyB": settings.MPESA_LIPA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://8938-105-163-27-172.ngrok-free.app//mpesa/callback/",  # Your callback URL
        "AccountReference": "Your Account Reference",
        "TransactionDesc": "Payment description"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    return response.json()    
