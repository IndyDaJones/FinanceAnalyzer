from numpy import exp
import numpy as np
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import logger as logger
from sql_connector import MySQL

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
        counter = 0;
        for stock in symbols:
           
            sql_query  = "SELECT Date, AdjClose FROM Stocks_Day_Test WHERE Symbol = '"+stock+"' ORDER BY Date"
            ticker = pd.read_sql(sql_query,connection)
            if (counter == 0):
                portfolio_matrix['Date'] = ticker['Date']
                portfolio_matrix[stock] = ticker['AdjClose']
            else:
                portfolio_matrix[stock] = ticker['AdjClose']
        
            counter = counter + 1;

        print(portfolio_matrix)
        portfolio_matrix = portfolio_matrix.set_index('Date') 
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