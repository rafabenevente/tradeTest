import yfinance as yf
import os

def get_stock_data(ticker, start_date, end_date):
    """
    Get stock data from Yahoo Finance.
    """
    tk = yf.Ticker(ticker)
    data = tk.history(start=start_date, end=end_date, interval='1d')
    return data

if __name__ == "__main__":
  os.makedirs('stocks', exist_ok=True)
  tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "FB", 
             "GOOG", "NVDA", "BRK-B", "JPM", "JNJ", "UNH", 
             "HD", "V", "BAC", "PG", "MA", "DIS", "ADBE"]
  for ticker in tickers:
    data = get_stock_data(ticker, "2018-01-01", "2021-10-31")
    data.drop(columns=['Dividends', 'Stock Splits'], inplace=True, errors='ignore')
    ticker_output = ticker.replace(".", "_")
    data.to_csv(f"stocks/{ticker_output}.csv")