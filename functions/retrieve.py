import pandas as pd
import yfinance as yf


def init(fromCSV = False, numberOfStocks = 10, daysSince=14):

    print(f"Requested days: {daysSince}.\nRequested stocks: {numberOfStocks}.")

    tickers_df = pd.read_csv('data/sp500_tickers.csv').head(numberOfStocks)
    tickers_df.set_index('Ticker', inplace=True)
    tickers_df.sort_values(by='Ticker', inplace=True)

    tickers_string = ' '.join(tickers_df.index.values)
    ts_today = pd.to_datetime('today')
    ts_origin = ts_today - pd.Timedelta(days=daysSince)


    downloadedData = yf.download(tickers_string, start=ts_origin, end=ts_today).fillna(0)
    return (downloadedData)

