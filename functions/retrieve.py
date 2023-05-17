import pandas as pd
import yfinance as yf

def read_tickers(numberOfStocks=10):
    tickers_df = pd.read_csv('data/sp500_tickers.csv').head(numberOfStocks)
    tickers_df.set_index('Ticker', inplace=True)
    tickers_df.sort_values(by='Ticker', inplace=True)

    tickers_string = ' '.join(tickers_df.index.values)

    return (tickers_string)

def get_timestamps(daysSince):
    ts_today = pd.to_datetime('today')
    ts_origin = ts_today - pd.Timedelta(days=daysSince)

    return (ts_today, ts_origin)

def get_downloaded_data(numberOfStocks = 10, daysSince=14):

    print(f"Requested days: {daysSince}.\nRequested stocks: {numberOfStocks}.")

    (tickers_string) = read_tickers(numberOfStocks)
    (ts_today, ts_origin) = get_timestamps(daysSince)

    downloadedData = yf.download(tickers_string, start=ts_origin, end=ts_today).fillna(0)
    return (downloadedData)

