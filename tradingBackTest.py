import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
from tradingFuncs import *

hood = yf.Ticker("googl")
historical = hood.history(start="2023-04-01", end="2023-06-07", interval="1h")
historical['SMA'] = sma(20, historical, "Close")
historical['Trend'] = highLow(historical, 3)
historical['Gap'] = gapIdentify(historical)
historical['VolSMA'] = sma(10, historical, "Volume")
historical['ATR'] = sma(10, historical, "ATR")

stopLossList = []

mybank = makeBank(400)
stock = openPosition('aapl')
amount = 1
price = historical['Close']

x = 0
while x < (len(historical)-1):
    for stop in stopLossList:
        if price[x] <= stop.price:
            print(historical.index[x+1])
            sell(stock, stop.amnt, price[x+1], mybank)
            print("Stoploss requirement met. Sold at " + str(price[x+1]) + ". Profit: " + str(price[x+1] - stock.averagePrice))
            stopLossList.remove(stop)
    
    if(historical['Volume'][x] > 1.5*historical['VolSMA'][x]):
        if(historical['Gap'][x] == "low"):
            if(buy(stock, 2 * amount, price[x+1], mybank)):
                print(historical.index[x+1])
                print("Buy:     " + str(2 * amount) + " shares " + str(price[x+1]))
                stop = stopLoss(0.90 * price[x+1], 2 * amount)
                print("Stoploss set at:  " + str(0.95 * price[x+1]))
                stopLossList.append(stop)

        elif(historical['Gap'][x] == "high"):
            if(sell(stock, amount, price[x+1], mybank)):
                print(historical.index[x+1])
                print("Sell:    " + str(amount) + " shares " + str(price[x+1]) + ". Profit: " + str(price[x+1] - stock.averagePrice))
                stopLossList[0].amnt -= 1
                if stopLossList[0].amnt == 0:
                    print("Stoploss at       " + str(stopLossList[0].price) + " removed")
                    stopLossList.remove(stopLossList[0])
    x += 1

if(stock.amnt > 0):
    sell(stock, stock.amnt, price[x], mybank)

print(mybank.cash)

