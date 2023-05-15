import pandas as pd
import yfinance as yf


def init(fromCSV = False, numberOfStocks = 10, daysSince=14, typeDate='Close'):

    if (fromCSV == True):
        print ("Returning stored data.")
        return ((pd.read_csv('data/rawdata.csv')).set_index('Date'))

    print(f"Requested days: {daysSince}.\nRequested stocks: {numberOfStocks}.\nData type: {typeDate}.")

    tickers_df = pd.read_csv('data/sp500_tickers.csv').head(numberOfStocks)
    tickers_df.set_index('Ticker', inplace=True)
    tickers_df.sort_values(by='Ticker', inplace=True)

    tickers_string = ' '.join(tickers_df.index.values)
    ts_today = pd.to_datetime('today')
    ts_origin = ts_today - pd.Timedelta(days=daysSince)


    return (yf.download(tickers_string, start=ts_origin, end=ts_today)[typeDate])

