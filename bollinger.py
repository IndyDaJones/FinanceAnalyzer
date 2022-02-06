import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import logger as logger
from sql_connector import MySQL
import matplotlib.pyplot as plt

def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down

def main():
    try:
        data = MySQL()
        connection = data.connect()

        symbols = data.loadTicker()

        logger.info("Get Info for: "+str(symbols))    
        start = dt.datetime(2021, 1, 1)
        logger.info("Start date: "+str(start))
        end = dt.datetime.now()
    
        logger.info("End date: "+str(end))
        #reset_Signals()
        
        for stock in symbols:
           
            sql_query  = "SELECT Date, Close FROM Stocks_Day_Test WHERE Symbol = '"+stock+"' ORDER BY Date ASC"
            ticker = pd.read_sql(sql_query,connection)
            

            symbol = stock
            #df = pdr.DataReader(symbol, 'yahoo', '2014-07-01', '2020-07-01')

            #df.index = np.arange(df.shape[0])
            ticker.index = np.arange(ticker.shape[0])
            closing_prices = ticker['Close'] # Why close and not Close Adj

            bollinger_up, bollinger_down = get_bollinger_bands(closing_prices)

            print(bollinger_down)


            plt.title(symbol + ' Bollinger Bands')
            plt.xlabel('Days')
            plt.ylabel('Closing Prices')
            plt.plot(closing_prices, label='Closing Prices')
            plt.plot(bollinger_up, label='Bollinger Up', c='g')
            plt.plot(bollinger_down, label='Bollinger Down', c='r')
            plt.legend()
            plt.show()


            #plot_graph(stock, ticker1, macd, exp3, buy_signal, sell_signal, macd_signal)

    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err  

#Main function
if __name__ == "__main__":
    main()