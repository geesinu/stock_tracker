from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, PriceHistory, Watchlist
from .forms import StockForm, StockSelectionForm
import json, requests, subprocess

# Create your views here.

def fetch_stock_news(symbol):
    """Fetch recent news articles for a specific stock symbol."""
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={settings.NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Limit to 5 recent articles
        return data['articles'][:5]
    return []


def calculate_change(new, old):
    """Helper function to calculate percentage change with + or - and 3 decimal places."""
    if old is None:
        return None
    change = ((new - old) / old) * 100
    # Format change to 3 decimal places and add + or - sign
    return f"{'+' if change > 0 else ''}{change:.3f}"


def calculate_moving_average(prices, days):
    """Calculates the moving average over the specified number of days."""
    if len(prices) < days:
        return None  # Not enough data points for the moving average
    return sum(prices[:days]) / days

def calculate_moving_average_series(prices, days):
    """Calculates a moving average series for each point, filling remaining slots with last value."""
    series = [
        sum(prices[i:i+days]) / days if len(prices[i:i+days]) == days else None 
        for i in range(len(prices))
    ]
    # Fill remaining slots with the last calculated value
    last_value = next((x for x in reversed(series) if x is not None), None)
    for i in range(len(series)):
        if series[i] is None:
            series[i] = last_value
    return series

def calculate_rsi(prices, period=14):
    """Calculates the Relative Strength Index (RSI) for the given period."""
    if len(prices) < period:
        return [None] * len(prices)  # Not enough data for RSI calculation

    rsi = []
    gains = []
    losses = []

    # Initial average gain/loss calculation for the first period
    for i in range(1, period + 1):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    # RSI calculation for the first period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi.append(100 - (100 / (1 + rs)))

    # RSI calculation for the remaining periods
    for i in range(period + 1, len(prices)):
        change = prices[i] - prices[i - 1]
        gain = change if change > 0 else 0
        loss = abs(change) if change < 0 else 0

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi.append(100 - (100 / (1 + rs)))

    # Extend the last calculated RSI value to the end of the list
    last_value = rsi[-1]
    rsi += [last_value] * (len(prices) - len(rsi))

    # Prepend None for initial period without RSI calculation
    rsi = [None] * (period - 1) + rsi
    return rsi


def stock_detail(request, symbol):
    # Retrieve the stock instance based on the symbol or return a 404 if not found
    stock = get_object_or_404(Stock, symbol=symbol)

    # Retrieve all historical prices for this stock, ordered by date in descending order
    history = PriceHistory.objects.filter(stock=stock).order_by('-date')

    # Fetch today's closing price
    today_price = history.first().close_price if history.exists() else None

    # Get the price 1 day ago, 7 days ago, and 30 days ago
    daily_change = None
    weekly_change = None
    monthly_change = None

    if len(history) > 1:
        daily_change = calculate_change(today_price, history[1].close_price)  # 1-day change

    week_ago_price = history.filter(date__gte=timezone.now() - timedelta(days=7)).last()
    if week_ago_price:
        weekly_change = calculate_change(today_price, week_ago_price.close_price)  # 7-day change

    month_ago_price = history.filter(date__gte=timezone.now() - timedelta(days=30)).last()
    if month_ago_price:
        monthly_change = calculate_change(today_price, month_ago_price.close_price)  # 30-day change

    # Prices list for calculating moving averages
    # Prepare data for the chart
    dates = [record.date.strftime("%Y-%m-%d") for record in history][::-1]  
    prices = [record.close_price for record in history][::-1] 
    volumes = [record.volume for record in history][::-1]   # Add volume data

    # Calculate RSI with a 14-day period
    rsi_series = calculate_rsi(prices, period=14)[::-1]
    rsi_series_json = json.dumps([float(value) if value is not None else None for value in rsi_series])



    # Calculate moving averages
    ma_5 = calculate_moving_average(prices, 5)
    ma_20 = calculate_moving_average(prices, 20)
    # Calculate moving average series
    ma_5_series = calculate_moving_average_series(prices, 5)[::-1] 
    ma_20_series = calculate_moving_average_series(prices, 20)[::-1] 


    # Fetch recent news articles for this stock
    news_articles = fetch_stock_news(stock.symbol)

    # Calculate All-Time High and Low
    all_time_high = history.order_by('-close_price').first()
    all_time_low = history.order_by('close_price').first()

    # Calculate 52-Week High and Low
    one_year_ago = timezone.now() - timedelta(weeks=52)
    year_history = history.filter(date__gte=one_year_ago)
    year_high = year_history.order_by('-close_price').first()
    year_low = year_history.order_by('close_price').first()


    # print("Dates:", dates)
    # print("Prices:", prices)
    # print("5-Day Moving Average:", ma_5_series)
    # print("20-Day Moving Average:", ma_20_series)

    context = {
        'stock': stock,
        'history': history,
        'daily_change': daily_change,
        'weekly_change': weekly_change,
        'monthly_change': monthly_change,
        'ma_5': ma_5,
        'ma_20': ma_20,
        'dates': dates,
        'prices': prices,
        'ma_5_series': ma_5_series,
        'ma_20_series': ma_20_series,
        'volumes': volumes,
        'rsi_series_json': rsi_series_json,
        'news_articles': news_articles,
        'all_time_high': all_time_high,
        'all_time_low': all_time_low,
        'year_high': year_high,
        'year_low': year_low,
    }

    # Pass stock details to the template for rendering
    return render(request, 'tracker/stock_detail.html', context)

@login_required
def add_to_watchlist(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    Watchlist.objects.get_or_create(user=request.user, stock=stock)
    return redirect('stock_detail', symbol=symbol)

@login_required
def remove_from_watchlist(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    Watchlist.objects.filter(user=request.user, stock=stock).delete()
    return redirect('profile')

@login_required
def add_stock(request):
    """
    View to add a new stock to the database.
    
    - Displays a form for the user to enter stock details.
    - Saves the form data to create a new stock record in the database.
    """
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile or another page after saving
    else:
        form = StockForm()
    return render(request, 'tracker/add_stock.html', {'form': form})

@login_required
def edit_stock(request, symbol):
    """
    View to update an existing stock's information.
    
    - Retrieves the stock based on its symbol.
    - Displays a form pre-filled with the stock's current data.
    - Saves any changes made to the stock's information.
    """
    stock = get_object_or_404(Stock, symbol=symbol)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StockForm(instance=stock)
    return render(request, 'tracker/edit_stock.html', {'form': form, 'stock': stock})

# @login_required
# def profile(request):
#     # Get the watchlist items for the currently logged-in user
#     watchlist_items = Watchlist.objects.filter(user=request.user)
#     # Check if the user is an admin (staff)
#     is_admin_user = request.user.is_staff

#     context = {
#         'watchlist_items': watchlist_items,
#         'is_admin_user': is_admin_user,
#     }
#     return render(request, 'tracker/profile.html', context)


def home_redirect(request):
    if request.user.is_authenticated:
        popular_stocks = Stock.objects.all()[::]
        watchlist_items = Watchlist.objects.filter(user=request.user)

        # Initialize the stock selection form for updating stocks
        stock_selection_form = StockSelectionForm()

        if request.method == 'POST' and 'edit_stock' in request.POST:
            stock_selection_form = StockSelectionForm(request.POST)
            if stock_selection_form.is_valid():
                selected_stock = stock_selection_form.cleaned_data['stock']
                return redirect('edit_stock', symbol=selected_stock.symbol)


        # Redirect to profile page if the user is logged in
        return render(request, 'tracker/profile.html', {
            'popular_stocks': popular_stocks,
            'watchlist_items': watchlist_items,
            'stock_selection_form': stock_selection_form,
        })

    else:
        # Redirect to login page if the user is not logged in
        return redirect('login')
    
def refresh_stock_data(request):
    """
    View to refresh stock data by calling the fetch_price_history management command.
    """
    try:
        # Run the management command to fetch stock data
        subprocess.call(['python', 'manage.py', 'fetch_price_history'])
        messages.success(request, "Stock data refreshed successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred while refreshing stock data: {e}")
    
    return redirect('profile')  # Redirect to the home page or any other page
    
def search_stock(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Stock.objects.filter(symbol__icontains=query) | Stock.objects.filter(name__icontains=query)
    return render(request, 'tracker/search_results.html', {'query': query, 'results': results})