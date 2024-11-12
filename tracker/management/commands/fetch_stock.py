from django.core.management.base import BaseCommand
from tracker.utils import fetch_stock_data

class Command(BaseCommand):
    help = 'Fetches stock data for a given symbol'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for')

    def handle(self, *args, **kwargs):
        symbol = kwargs['symbol']
        success = fetch_stock_data(symbol)

        if success:
            self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {symbol}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data for {symbol}"))
