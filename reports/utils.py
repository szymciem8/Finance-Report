import yfinance as yf
import pandas as pd


VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

def generate_finance_report(stock, period):
    if period not in VALID_PERIODS:
        period = '1mo'

    ticker = yf.Ticker(stock)

    df_yahoo = ticker.history(period=period)
    info_yahoo = ticker.info
    
    open_price = df_yahoo['Open'].values
    high_price = df_yahoo['High'].values
    low_price = df_yahoo['Low'].values
    close_price = df_yahoo['Close'].values
    volume = df_yahoo['Volume'].values
    date = df_yahoo.index.values

    short_name = info_yahoo.get('shortName', 'N/A')
    long_name = info_yahoo.get('longName', 'N/A')
    sector = info_yahoo.get('sector', 'N/A')
    website = info_yahoo.get('website', 'N/A')
    long_summary = info_yahoo.get('longBusinessSummary', 'N/A')

    current_price = ticker.analyst_price_target[0]['currentPrice']

    # Convert numpy datetime64 to datetime
    date = [pd.to_datetime(d).date().strftime('%Y-%m-%d') for d in date]

    context = {
        'stock': str(stock),
        'date': list(date),
        'open_price': list(open_price),
        'high_price': list(high_price),
        'low_price': list(low_price),
        'close_price': list(close_price),
        'volume': list(volume),
        'short_name': str(short_name),
        'long_name': str(long_name),
        'sector': str(sector),
        'website': str(website),
        'long_summary': str(long_summary),
        'current_price': f'{current_price:.2f}'
    }
    
    return context