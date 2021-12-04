from numpy import exp
import numpy as np
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

def implement_portfolio_matix(stock, ticker, data):
    print(ticker)
    print(data)    
    
    for index in ticker.index:
        try:
            ticker[stock][index] = data[index]
    
        except Exception as err:
            logger.error("Exception cauth"+str(err))
            print(f"Unexpected {err=}, {type(err)=}")
            print(err)
            raise err      

    return ticker

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
        portfolio_matrix = pd.DataFrame()
        logger.info("End date: "+str(end))
        for stock in symbols:
           
            sql_query  = "SELECT Date, AdjClose FROM Stocks_Day_Test WHERE Symbol = '"+stock+"' ORDER BY Date"
            ticker = pd.read_sql(sql_query,connection)

            portfolio_matrix[stock] = ticker['AdjClose']

        #percent_change = portfolio_matrix['ROG.SW'].pct_change().apply(lambda x: np.log(1+x))
        #print(percent_change)

        # Covariance Matrix
        cov_matrix = portfolio_matrix.pct_change().apply(lambda x: np.log(1+x)).cov()
        print(cov_matrix)

        # Correlation Matrix
        #corr_matrix = portfolio_matrix.pct_change().apply(lambda x: np.log(1+x)).corr()
        #print(corr_matrix)

        # Randomly weighted portfolio's variance
        w = {'SPICHA.SW': 0.3, 'NOW': 0.05, 'USSRS.SW': 0.1, 'SPMCHA.SW': 0.1, 'WZEC.F': 0.15, 'CSL.AX': 0.1, 'ROG.SW': 0.2}
        port_var = cov_matrix.mul(w, axis=0).mul(w, axis=1).sum().sum()
        print(port_var)

        # Yearly returns for individual companies
        ind_er = portfolio_matrix.resample('Y').last().pct_change().mean()
        print(ind_er)

        """
        # Variance
        variance = percent_change.var()
        print(variance)
        
        #Volatility:
        volatility = np.sqrt(variance * 250)
        print(volatility)

        # Covariance of two stocks
        percent_change['STOCK A'].cov(percent_change['STOCK B'])

        #Correlation of two stocks
        percent_change['STOCK A'].corr(percent_change['STOCK B'])

        # Expected Returns
        # Define weights for allocation
        w = [0.2, 0.8]
        e_r_ind = percent_change.mean()

        # Total expected return
        e_r = (e_r_ind*w).sum()
        """
            #plot_graph(stock, ticker1, macd, exp3, buy_signal, sell_signal, macd_signal)
    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err  

#Main function
if __name__ == "__main__":
    main()