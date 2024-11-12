from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),  # Redirects from the home page
    path('stocks/<str:symbol>/', views.stock_detail, name='stock_detail'),
    path('add_to_watchlist/<str:symbol>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<str:symbol>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('accounts/profile/', views.home_redirect, name='profile'),
    path('search/', views.search_stock, name='search_stock'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit_stock/<str:symbol>/', views.edit_stock, name='edit_stock'),
    path('refresh_stock_data/', views.refresh_stock_data, name='refresh_stock_data'),
]
