import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt

start = dt.datetime(2021, 10, 29)
end = dt.datetime.now()
ticker = pdr.get_data_yahoo("NOW", start, end)['Adj Close']

exp1 = ticker.ewm(span=12, adjust=False).mean()
exp2 = ticker.ewm(span=26, adjust=False).mean()
macd = exp1 - exp2
exp3 = macd.ewm(span=9, adjust=False).mean()
macd.plot(label='NOW MACD', color='g')
ax = exp3.plot(label='Signal Line', color='r')
ticker.plot(ax=ax, secondary_y=True, label='NOW')

ax.set_ylabel('MACD')
ax.right_ax.set_ylabel('Price $')
ax.set_xlabel('Date')
lines = ax.get_lines() + ax.right_ax.get_lines()
ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
plt.show()