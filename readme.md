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
   git clone https://github.com/geesinu/stock_tracker.git
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

## Usage

- **Home Page**: Displays stock information, popular stocks, and quick links to add/remove stocks from the watchlist.
- **Stock Details**: Displays detailed information for a selected stock, including:
   - Price Trend with 5-Day and 20-Day Moving Averages (toggleable).
   - Volume and RSI (14) charts.
   - Daily, Weekly, and Monthly Price Changes.
   - All-Time High/Low and 52-Week High/Low.
   - Recent news articles related to the stock.
- **Watchlist**: Users can add/remove stocks to/from their watchlist from the stock detail view.
- **Stock Management Features**: All authenticated users have access to add, edit, and refresh stock data.

## API & URL Endpoints
### Main URLs
 1. **Home Redirect** (`/`, name='home')
      - Redirects authenticated users to the profile page, displaying their watchlist and popular stocks.
 2. **Stock Detail**  (`/stocks/<symbol>/`, name='stock_detail')
      - Redirects authenticated users to the profile page, displaying their watchlist and popular stocks.
 3. **Add to Watchlist**  (`/add_to_watchlist/<symbol>/`, name='add_to_watchlist')
      - Adds a specified stock to the user’s watchlist.
 4. **Remove from Watchlist**  (`/remove_from_watchlist/<symbol>/`, name='remove_from_watchlist')
      - Removes a specified stock from the user’s watchlist.
 5. **Profile**  (`/accounts/profile/`, name='profile')
      - Profile page that displays the user’s watchlist and stock management options.
 6. **Search Stock**  (`/search/`, name='search_stock')
      - Search functionality to find stocks by symbol or name.
### Stock Management URLs
 7. **Add Stock**  (`/add_stock/`, name='add_stock')
      - Allows users to add new stocks to the database. Displays a form with fields for stock symbol, name, and sector.
 8. **Edit Stock**  (`/edit_stock/<symbol>/`, name='edit_stock')
      - Allows users to edit details of an existing stock. Users select the stock to edit from a dropdown on the profile page.
 9. **Refresh Stock Data**  (`/refresh_stock_data/`, name='refresh_stock_data')
      - Triggers the `fetch_price_history` management command to update stock price data.

## Future Improvements
- **Financial Ratios**: Calculation and display of P/E, P/B, and Dividend Yield ratios.
- **User Sentiment Analysis**: Allow users to submit sentiment (bullish or bearish) on each stock, with an overall sentiment summary displayed.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
