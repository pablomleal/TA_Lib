def init(numberOfStocks = 10, daysSince=14, typeDate='Close'):
    #defaultKwargs = { 'numberOfStocks': 10, 'daysSince': 14, 'typeDate': 'Close' }
    #kwargs = { **defaultKwargs, **kwargs }
    print(f"Requested days: {daysSince}.\nRequested stocks: {numberOfStocks}.\nData type: {typeDate}.")

    tickers_df = pd.read_csv('sp500_tickers.csv').head(numberOfStocks)
    tickers_df.set_index('Ticker', inplace=True)
    tickers_df.sort_values(by='Ticker', inplace=True)

    tickers_string = ' '.join(tickers_df.index.values)
    ts_today = pd.to_datetime('today')
    ts_origin = ts_today - pd.Timedelta(days=daysSince)

    return (yf.download(tickers_string, start=ts_origin, end=ts_today)[typeDate])
    