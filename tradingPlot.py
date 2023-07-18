import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import pandas as pd
import tradingFuncs as tf
from operator import sub
from datetime import datetime, timedelta

stock = yf.Ticker("aapl")

historical = stock.history(start="2023-03-01", interval="1h")

historical['SMA'] = tf.sma(20, historical, "Close")
historical['Trend'] = tf.highLow(historical, 3)
historical['Gap'] = tf.gapIdentify(historical)
historical['VolSMA'] = tf.sma(10, historical, "Volume")
historical['ATR'] = tf.sma(10, historical, "ATR")
 


tf.candleStickPlot(historical)

# x = 0
# #print(historical.to_string())
# while x < len(historical):
#     if(historical['Volume'][x] > 1.5*historical['VolSMA'][x]):
#       if(historical['Gap'][x] == "low"):
#         plt.axvline(x = historical.index[x], color = 'green', linewidth = 0.5, linestyle = '-.')
#       elif (historical['Gap'][x] == "high"):
#         plt.axvline(x = historical.index[x], color = 'red', linewidth = 0.5, linestyle = '-.')
#     x += 1

#historical.plot(y=['Volume', 'VolSMA'])
plt.show()