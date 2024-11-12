import requests
from datetime import datetime
from .models import Stock, PriceHistory
from django.conf import settings

def fetch_stock_data(symbol):
    # Base URL for Alpha Vantage API
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={settings.ALPHA_VANTAGE_API_KEY}'
    
    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Check if the API response contains data
    if "Time Series (Daily)" in data:
        # Get or create the Stock object in the database
        stock, created = Stock.objects.get_or_create(symbol=symbol)

        # Iterate over each date in the historical data
        for date, price_data in data["Time Series (Daily)"].items():
            # Parse date
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            # Store historical prices in the database
            PriceHistory.objects.update_or_create(
                stock=stock,
                date=date_obj,
                defaults={
                    'open_price': price_data['1. open'],
                    'close_price': price_data['4. close'],
                    'volume': price_data['5. volume']
                }
            )
        return True
    else:
        print("Error fetching data:", data.get("Error Message", "Unknown error"))
        return False
