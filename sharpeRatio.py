import re
from numpy import exp
import numpy as np
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import logger as logger
from sql_connector import MySQL

def getDateValue(ticker, date):
    returnValue = np.nan
    for index in ticker.index:
        try:
            #print(ticker['Date'][index])
            #print(date)
            if ticker['Date'][index] == date:
                #print(ticker['AdjClose'][index])
                returnValue = ticker['AdjClose'][index]
        
        except Exception as err:
            logger.error("Exception cauth"+str(err))
            print(f"Unexpected {err=}, {type(err)=}")
            print(err)
            raise err
    
    return returnValue

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
                
        sql_query  = "SELECT DISTINCT Date FROM Stocks_Day_Test WHERE Status = 'OK' ORDER BY Date ASC"
        portfolio_matrix = pd.read_sql(sql_query,connection)
        #portfolio_matrix['Date'] = ticker['Date']
                
        logger.info("End date: "+str(end))
        counter = 0;
        for stock in symbols:
           
            sql_query  = "SELECT Date, AdjClose FROM Stocks_Day_Test WHERE Status = 'OK' AND Symbol = '"+stock+"' ORDER BY Date ASC"
            ticker = pd.read_sql(sql_query,connection)

            for index in portfolio_matrix.index:
                try:
                    value = getDateValue(ticker, portfolio_matrix['Date'][index])
                    portfolio_matrix.loc[portfolio_matrix.index[index], stock] = value
                
                except Exception as err:
                    logger.error("Exception cauth"+str(err))
                    print(f"Unexpected {err=}, {type(err)=}")
                    print(err)
                    raise err

            portfolio_matrix[stock] = portfolio_matrix[stock].fillna(method='pad')

        portfolio_matrix['Date'] = pd.to_datetime(portfolio_matrix['Date'], errors = 'ignore')
        portfolio_matrix = portfolio_matrix.set_index('Date') 
        # Covariance Matrix
        cov_matrix = portfolio_matrix.pct_change().apply(lambda x: np.log(1+x)).cov()

        # Correlation Matrix
        #corr_matrix = portfolio_matrix.pct_change().apply(lambda x: np.log(1+x)).corr()
        #print(corr_matrix)

        # Eeighted portfolio's variance
        #w = {'SPICHA.SW': 0.3, 'NOW': 0.05, 'USSRS.SW': 0.1, 'SPMCHA.SW': 0.1, 'WZEC.F': 0.15, 'CSL.AX': 0.1, 'ROG.SW': 0.1, '1704395.SW': 0.1}
        w = {'SPICHA.SW': 0.3, 'NOW': 0.05, 'USSRS.SW': 0.1, 'SPMCHA.SW': 0.1, 'WZEC.F': 0.15, 'CSL.AX': 0.1, 'ROG.SW': 0.2}
        port_var = cov_matrix.mul(w, axis=0).mul(w, axis=1).sum().sum()
        
        # Yearly returns for individual companies
        #ind_er = portfolio_matrix.resample('Y').last().pct_change().mean()
        ind_er = portfolio_matrix.resample('Y').last().pct_change().mean()
        
        # Portfolio returns
        for index in ind_er.index:
            ind_er[index] = w[index]*ind_er[index] 
        port_er = (ind_er).sum()
        
        # Volatility is given by the annual standard deviation. We multiply by 250 because there are 250 trading days/year.
        ann_sd = portfolio_matrix.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
        assets = pd.concat([ind_er, ann_sd], axis=1) # Creating a table for visualising returns and volatility of assets
        assets.columns = ['Returns', 'Volatility']
        
        p_ret = [] # Define an empty array for portfolio returns
        p_vol = [] # Define an empty array for portfolio volatility
        p_weights = [] # Define an empty array for asset weights

        num_assets = len(portfolio_matrix.columns)
        num_portfolios = 10000

        for portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights = weights/np.sum(weights)
            p_weights.append(weights)
            returns = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its 
                                      # weights 
            p_ret.append(returns)
            var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
            sd = np.sqrt(var) # Daily standard deviation
            ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
            p_vol.append(ann_sd)

        data = {'Returns':p_ret, 'Volatility':p_vol}

        for counter, symbol in enumerate(portfolio_matrix.columns.tolist()):
            #print(counter, symbol)
            data[symbol+' weight'] = [w[counter] for w in p_weights]

        portfolios  = pd.DataFrame(data)
        portfolios.head() # Dataframe of the 10000 portfolios created

        # Plot efficient frontier
        portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])

        min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
        # idxmin() gives us the minimum value in the column specified.                               
        
        # plotting the minimum volatility portfolio
        plt.subplots(figsize=[10,10])
        plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=10, alpha=0.3)
        plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)

        # Finding the optimal portfolio
        rf = 0.01 # risk factor
        optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
        
        # Plotting optimal portfolio
        plt.subplots(figsize=(10, 10))
        plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=10, alpha=0.3)
        plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
        plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
        plt.show()

            #plot_graph(stock, ticker1, macd, exp3, buy_signal, sell_signal, macd_signal)
    except Exception as err:
        logger.error("Exception cauth"+str(err))
        print(f"Unexpected {err=}, {type(err)=}")
        raise err  

#Main function
if __name__ == "__main__":
    main()