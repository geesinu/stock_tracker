from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class PriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)  # Use a string reference

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'stock'], name='unique_user_stock')
        ]
