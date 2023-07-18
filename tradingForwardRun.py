import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
from tradingFuncs import *
import schedule
import pandas_market_calendars
import twilio

hood = yf.Ticker("googl")
historical = hood.history(start="2023-04-01", end="2023-06-07", interval="1h")
historical['SMA'] = sma(20, historical, "Close")
historical['Trend'] = highLow(historical, 3)
historical['Gap'] = gapIdentify(historical)
historical['VolSMA'] = sma(10, historical, "Volume")
historical['ATR'] = sma(10, historical, "ATR")