# Stock Market Tracker

A Django-based Stock Market Tracker that provides detailed insights into selected stocks. Users can view historical stock data, track moving averages, analyze Relative Strength Index (RSI), check recent news, and add stocks to a personalized watchlist.

This project showcases advanced Django functionality, API integration, and dynamic data visualization, highlighting skills in Python, Django, and web development.

## Features

- **Stock Details**: View historical prices, moving averages, and RSI for individual stocks.
- **News Integration**: Displays recent news articles related to each stock.
- **Watchlist**: Allows users to add stocks to their watchlist for quick access.
- **Add Stock**: Users can add new stocks to the database.
- **Edit Stock**: Users can select an existing stock to update its details.
- **Refresh Stock Data**: A button on the homepage triggers the fetching of the latest stock data.
- **User Authentication**: Includes login and registration with personalized profile pages.
- **Historical Highs and Lows**: Displays all-time and 52-week high and low prices for each stock.
- **Future Work**: Planned features include Simple Financial Ratios (P/E, P/B, Dividend Yield) and User Sentiment Analysis.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Data Visualization**: Chart.js
- **API Integration**: Alpha Vantage API, News API (or similar) for stock market data and stock-related news

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/stock-market-tracker.git
   cd stock-market-tracker
   ```

2. **Create and Activate a conda Environment**:

   ```bash
   conda create -n your_environment_name --file requirements.txt
   conda activate your_environment_name
   ```

3. **API Key Configuration**:
   Obtain an API key from Alpha Vantage API (https://www.alphavantage.co/) and News API (https://newsapi.org/).
   Add the API key to settings.py:

   ```python
   ALPHA_VANTAGE_API_KEY = "your_api_key_here"
   NEWS_API_KEY = "your_api_key_here"
   ```

4. **Database Migration**:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (for admin access)**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:

- Go to http://127.0.0.1:8000 in your browser.

**Usage**

- Home Page: Displays stock information, popular stocks, and quick links to add/remove stocks from the watchlist.
- Stock Details: View detailed information, including historical prices, moving averages, RSI, news, and highs and lows.
- Profile Page: View and manage your watchlist.
- Admin Panel: Admin users can access the admin panel at /admin to manage stocks, news, and other app data.
