import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period='1y', interval='1d'):
    """
    Fetch historical stock data for a given ticker using Yahoo Finance API.
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str): Data period (e.g., '1y', '2y').
        interval (str): Data interval (e.g., '1d', '1wk').
    Returns:
        pd.DataFrame: Historical stock data.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        return hist
    except Exception as e:
        raise ValueError(f"Failed to fetch data for {ticker}: {e}")

# Example usage
if __name__ == "__main__":
    ticker = 'AAPL'
    data = get_stock_data(ticker)
    print(data.head())
