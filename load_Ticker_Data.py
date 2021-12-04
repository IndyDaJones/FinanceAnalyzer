
from sql_connector import MySQL
import logger as logger
import datetime as dt
import pandas_datareader as pdr

def persist_data(stock, tickers, createdate):
    try:
        data = MySQL()
        data.connect()
        for dates in tickers.index:
            for info in tickers:
                if info == "High":
                    high = tickers[info][dates]
                elif info == "Low":
                    low = tickers[info][dates]
                elif info == "Open":
                    open = tickers[info][dates]
                elif info == "Close":
                    close = tickers[info][dates]
                elif info == "Volume":
                    volume = tickers[info][dates]
                elif info == "Adj Close":
                    adjclose = tickers[info][dates]
                else:
                    print("Hi")
            data.persistData(stock, "EQUITY", "USD", open, high, low, close, adjclose, volume, dates, createdate)
        data.disconnect()
    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err

def main():
    try:
        data = MySQL()
        connection = data.connect()
        symbols = data.loadTicker()
        logger.info("Get Info for: "+str(symbols))    
        start = dt.datetime(2021, 1, 1)
        logger.info("Start date: "+str(start))
        #yesterday = dt.datetime.now() - dt.timedelta(1)
        yesterday = dt.datetime.now()

        logger.info("End date: "+str(yesterday))
        for stock in symbols:
            # Read Data
            logger.info("Get ticker data: "+stock) 
            print(stock)   
            ticker = pdr.get_data_yahoo(stock, start, yesterday)
            print(len(ticker['Adj Close']))
            persist_data(stock, ticker, yesterday.strftime("%Y-%m-%d %H:%M:%S"))
            
    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err  

#Main function
if __name__ == "__main__":
    main()