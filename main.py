from numpy import exp
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import logger as logger

def print_data(array):   
    for index in array.index:
        print(index, array[index])

def print_recommendations(array):   
    for index in range(len(array)):
        if array[index][0] != 0:
            print(array[index][0], array[index][1])

def get_stock_data(symbols,start, end):
    return pdr.DataReader(symbols, 'yahoo', start=start, end=end)
    

#‘implement_macd_strategy’ which takes the stock prices (‘data’), and MACD data (‘data’) as parameters
def implement_macd_strategy(prices, macd, signal_data):    
    buy_price = {}
    sell_price = {}
    macd_signal = {}
    signal = 0

    for index in prices.index:
        if macd[index] > signal_data[index]:
            if signal != 1:
                buy_price[index] = prices[index]
                signal = 1
                macd_signal[index] = signal
        elif macd[index] < signal_data[index]:
            if signal != -1:
                sell_price[index] = prices[index]
                signal = -1
                macd_signal[index] = signal
           
    return buy_price, sell_price, macd_signal

def plot_graph(stock, ticker, macd, exp3, buy_price, sell_price, macd_signal):
    macd.plot(label=stock+' MACD', color='g')
    ax = exp3.plot(label='Signal Line', color='r')
    ticker.plot(ax=ax, secondary_y=True, label=stock)

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
    ax.plot(ticker, color = 'skyblue', linewidth = 2, label = stock)
    ax.plot(ticker.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax.plot(ticker.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
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
def claculate_macd(ticker_data):
    exp1 = ticker_data.ewm(span=12, adjust=False).mean()
    exp2 = ticker_data.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean() 
    return macd, exp3

def main():
    symbols = {'SPICHA.SW','SPMCHA.SW','WZEC.F','ROG.SW','NOW','CSL.AX','USSRS.SW'} 
    logger.info("Get Info for: "+str(symbols))    
    start = dt.datetime(2021, 1, 1)
    logger.info("Start date: "+str(start))
    end = dt.datetime.now()
    logger.info("End date: "+str(end))
    for stock in symbols:
        # Read Data
        #ticker = pdr.DataReader(stock, 'yahoo', start=start, end=end)
        #ticker = pdr.get_data_yahoo(stock, start, end)['Adj Close']
        #Date       High         Low        Open       Close     Volume   Adj Close
        logger.info("Get ticker data: "+stock)    
        ticker = pdr.get_data_yahoo(stock, start, end)
        macd, exp3 = claculate_macd(ticker['Adj Close'])
        buy_price, sell_price, macd_signal = implement_macd_strategy(ticker['Adj Close'], macd, exp3)

        print("Stock: "+ stock +"\n")
        print("BUY: \n"+ str(buy_price) +"\n")
        print("SELL: \n"+ str(sell_price) +"\n")

        plot_graph(stock, ticker['Adj Close'], macd, exp3, buy_price, sell_price, macd_signal)

#Main function
if __name__ == "__main__":
    main()