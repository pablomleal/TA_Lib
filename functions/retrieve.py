import pandas as pd
import yfinance as yf




def get_tickers(numberOfStocks=10):
    tickers_df = pd.read_csv('data/sp500_tickers.csv').head(numberOfStocks)
    tickers_df.set_index('Ticker', inplace=True)
    tickers_df.sort_values(by='Ticker', inplace=True)

    return (tickers_df)

def get_timestamps(daysSince):
    ts_today = pd.to_datetime('today')
    ts_origin = ts_today - pd.Timedelta(days=daysSince)

    return (ts_today, ts_origin)

def get_downloaded_data(tickers_df, numberOfStocks = 10, daysSince=14):
    print("Initiating download...")
    print(f"--> Requested days: {daysSince}.\n--> Requested stocks: {numberOfStocks}.")
    tickers_string = ' '.join(tickers_df.index.values)
    (ts_today, ts_origin) = get_timestamps(daysSince)
    downloadedData = yf.download(tickers_string, start=ts_origin, end=ts_today).fillna(0)
    return (downloadedData)

def distribute_data(downloadedData):
    rawdata = downloadedData['Close']
    spreads = (downloadedData['High'] - downloadedData['Low'])/(downloadedData['Close'])
    volumes = downloadedData['Volume']
    highs = downloadedData['High']
    lows =  downloadedData['Low']
    return (rawdata, spreads, volumes, highs, lows)

def save_data(rawdata, spreads, volumes, highs, lows):
    rawdata.to_csv('./data/close.csv')
    spreads.to_csv('./data/spreads.csv')
    volumes.to_csv('./data/volumes.csv')
    highs.to_csv('./data/highs.csv')
    lows.to_csv('./data/lows.csv')

def from_CSV(daysSince, numberOfStocks):
    
    #Retrieving stored data
    closes_saved = pd.read_csv('./data/close.csv').set_index('Date')
    
    #Checking same indices
    ts_origin = pd.to_datetime('today') - pd.Timedelta(days=daysSince)
    is_same_dates = ts_origin.strftime('%Y-%m-%d') == closes_saved.index[0]

    #Checking same number of columns (stocks)
    is_same_number_of_stocks = closes_saved.shape[1] == numberOfStocks
    
    print (f"Is it possible to use cached data? {is_same_dates & is_same_number_of_stocks}")
    return (is_same_dates & is_same_number_of_stocks)

def get_from_CSV():
        print ("Returning stored data.")
        rawdata = (pd.read_csv('data/close.csv')).set_index('Date')
        spreads = (pd.read_csv('data/spreads.csv')).set_index('Date')
        volumes = (pd.read_csv('data/volumes.csv')).set_index('Date')
        highs = (pd.read_csv('data/highs.csv')).set_index('Date')
        lows = (pd.read_csv('data/lows.csv')).set_index('Date')
        return (rawdata, spreads, volumes, highs, lows)