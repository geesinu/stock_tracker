# tracker/management/commands/import_popular_stocks.py

from django.core.management.base import BaseCommand
from tracker.models import Stock

class Command(BaseCommand):
    help = 'Imports a list of popular stocks into the database'

    def handle(self, *args, **kwargs):
        # List of popular stocks with sectors
        stocks = [
            {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Communication Services"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology"},
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials"},
            {"symbol": "V", "name": "Visa Inc.", "sector": "Financials"},
            {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Health Care"},
            {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples"},
            {"symbol": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Staples"},
            {"symbol": "DIS", "name": "The Walt Disney Company", "sector": "Communication Services"},
            {"symbol": "MA", "name": "Mastercard Inc.", "sector": "Financials"},
            {"symbol": "PYPL", "name": "PayPal Holdings Inc.", "sector": "Financials"},
            {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
            {"symbol": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy"},
            {"symbol": "KO", "name": "The Coca-Cola Company", "sector": "Consumer Staples"},
            {"symbol": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Staples"},
            {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Health Care"},
            {"symbol": "MRK", "name": "Merck & Co., Inc.", "sector": "Health Care"},
            {"symbol": "ABT", "name": "Abbott Laboratories", "sector": "Health Care"},
            {"symbol": "T", "name": "AT&T Inc.", "sector": "Communication Services"},
            {"symbol": "BA", "name": "The Boeing Company", "sector": "Industrials"}
        ]

        # Add each stock to the database
        for stock_data in stocks:
            Stock.objects.update_or_create(
                symbol=stock_data["symbol"],
                defaults={"name": stock_data["name"], "sector": stock_data["sector"]}
            )

        self.stdout.write(self.style.SUCCESS("Successfully imported popular stocks"))
