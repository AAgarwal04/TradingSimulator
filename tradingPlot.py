import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import pandas as pd
import tradingFuncs as tf
from operator import sub
from datetime import datetime, timedelta

stock = yf.Ticker("aapl")

historical = stock.history(start="2022-02-01", interval="1d")

historical['5SMA'] = tf.sma(5, historical, "Close")
historical['10SMA'] = tf.sma(10, historical, "Close")
historical['20SMA'] = tf.sma(20, historical, "Close")
 


#tf.candleStickPlot(historical)

historical.plot(y=['Close', '5SMA', '10SMA', '20SMA'])

x = 0
flag = 0
#print(historical.to_string())
while x < len(historical):
    if(historical['5SMA'][x] > historical['10SMA'][x] and historical['5SMA'][x] > historical['20SMA'][x]):
      if(flag == 0):
        plt.axvline(x = historical.index[x], color = 'green', linewidth = 0.5, linestyle = '-.')
        flag = 1
    elif(historical['5SMA'][x] < historical['10SMA'][x] or historical['5SMA'][x] < historical['20SMA'][x]):
      if(flag == 1):
        plt.axvline(x = historical.index[x], color = 'red', linewidth = 0.5, linestyle = '-.')
        flag = 0
    x += 1

plt.show()