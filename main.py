from numpy import exp
import numpy 
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import logger as logger
from sql_connector import MySQL

def print_data(array):   
    for index in array.index:
        print(index, array[index])

def print_recommendations(array):   
    for index in range(len(array)):
        if array[index][0] != 0:
            print(array[index][0], array[index][1])

def get_stock_data(symbols,start, end):
    return pdr.DataReader(symbols, 'yahoo', start=start, end=end)

def implement_macd_strategy_yahoo(prices, macd, signal_data):    
    buy_signal = {}
    sell_signal = {}
    macd_signal = {}
    signal = 0

    for index in prices.index:
        try:
            if macd[index] > signal_data[index]:
                if signal != 1:
                    buy_signal[index] = prices[index]
                    signal = 1
                    macd_signal[index] = signal
            
            elif macd[index] < signal_data[index]:
                if signal != -1:
                    sell_signal[index] = prices[index]
                    signal = -1
                    macd_signal[index] = signal
        
        except Exception as err:
            logger.error("Exception cauth"+str(err))
            print(f"Unexpected {err=}, {type(err)=}")
            print(err)
            raise err      

    return buy_signal, sell_signal, macd_signal 

#‘implement_macd_strategy’ which takes the stock prices (‘data’), and MACD data (‘data’) as parameters
def implement_macd_strategy(prices, macd, signal_data):    
    buy_signal = {}
    sell_signal = {}
    macd_signal = {}
    signal = 0

    for index in prices.index:
        try:
            if macd['AdjClose'][index] > signal_data['AdjClose'][index]:
                if signal != 1:
                    buy_signal[prices['Date'][index]] = prices['AdjClose'][index]
                    signal = 1
                    macd_signal[prices['Date'][index]] = signal
            
            elif macd['AdjClose'][index] < signal_data['AdjClose'][index]:
                if signal != -1:
                    sell_signal[prices['Date'][index]] = prices['AdjClose'][index]
                    signal = -1
                    macd_signal[prices['Date'][index]] = signal
        
        except Exception as err:
            logger.error("Exception cauth"+str(err))
            print(f"Unexpected {err=}, {type(err)=}")
            print(err)
            raise err      

    return buy_signal, sell_signal, macd_signal

def plot_graph(stock, ticker, macd, exp3, buy_price, sell_price, macd_signal):
    macd.plot(label=stock+' MACD', color='g')
    ax = exp3.plot(label='Signal Line', color='r')
    ticker['AdjClose'].plot(ax=ax, secondary_y=True, label=stock)

    ax.set_ylabel('MACD')
    ax.right_ax.set_ylabel('Price $')
    ax.set_xlabel('Date')
    lines = ax.get_lines() + ax.right_ax.get_lines()
    ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
    plt.show()

    #BUY and SELL Plot
    #ax = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    #ax = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    """
    ax.plot(ticker['AdjClose'], color = 'skyblue', linewidth = 2, label = stock)
    ax.plot(ticker['AdjClose'].index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax.plot(ticker['AdjClose'].index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
    ax.legend()
    ax.set_title('MACD SIGNALS')
    ax.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax.plot(macd_signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    
    for i in range(len(googl_macd)):
        if str(googl_macd['hist'][i])[0] == '-':
            ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color = '#ef5350')
        else:
            ax2.bar(googl_macd.index[i], googl_macd['hist'][i], color = '#26a69a')
    
    
    plt.legend(loc = 'lower right')
         
    plt.show()
    """
def reset_Signals():
    try:
        data = MySQL()
        data.connect()
        data.resetSignal()
        data.disconnect()

    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err

def update_signal(signal_type, stock, signal_data):
    try:
        data = MySQL()
        data.connect()
        for dates in signal_data:
            data.updateSignal(dates, stock, signal_type)

        data.disconnect()
    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err

def claculate_macd(ticker_data):
    exp1 = ticker_data.ewm(span=12, adjust=False).mean()
    exp2 = ticker_data.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean() 
    return macd, exp3

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
        reset_Signals()
        
        for stock in symbols:
           
            sql_query  = "SELECT Date, AdjClose FROM Stocks_Day_Test WHERE Symbol = '"+stock+"' ORDER BY Date ASC"
            ticker = pd.read_sql(sql_query,connection)
            
            macd, exp3 = claculate_macd(ticker)
            buy_signal, sell_signal, macd_signal = implement_macd_strategy(ticker, macd, exp3)

            update_signal("BUY", stock, buy_signal)
            update_signal("SELL", stock, sell_signal)

            #plot_graph(stock, ticker1, macd, exp3, buy_signal, sell_signal, macd_signal)

    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err  

#Main function
if __name__ == "__main__":
    main()