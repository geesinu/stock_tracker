from django.contrib import admin
from .models import Stock, PriceHistory, Watchlist

# Register your models here.
admin.site.register(Stock)
admin.site.register(PriceHistory)
admin.site.register(Watchlist)