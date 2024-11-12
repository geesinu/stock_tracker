# tracker/management/commands/fetch_price_history.py

from django.core.management.base import BaseCommand
from tracker.models import Stock
from tracker.utils import fetch_stock_data

class Command(BaseCommand):
    help = 'Fetches and stores price history for all stocks in the database'

    def handle(self, *args, **kwargs):
        stocks = Stock.objects.all()[::]
        for stock in stocks:
            success = fetch_stock_data(stock.symbol)
            if success:
                self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {stock.symbol}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data for {stock.symbol}"))
