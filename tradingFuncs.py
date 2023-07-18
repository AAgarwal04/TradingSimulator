import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta


#Functions for BackTesting

class ticker(object):
    name = ""
    amnt = 0
    averagePrice = 0

    def __init__(self, stockName):
        self.name = stockName

class bank(object):
    cash = 0

    def __init__(self, cashAmount):
        self.cash = cashAmount

class stopLoss(object):
    def __init__(self, price, amnt):
        self.price = price
        self.amnt = amnt


def makeBank(cashAmount):
    newBank = bank(cashAmount)
    return newBank

def openPosition(position):
    stock = ticker(ticker)
    return stock

def buy(stock, amount, price, bank):
    if bank.cash >= (amount * price):
        stock.averagePrice = ((stock.averagePrice * stock.amnt) + (amount * price))/(amount + stock.amnt)
        stock.amnt += amount
        bank.cash -= (amount * price)
        return True
    else:
        return False

def sell(stock, amount, price, bank):
    if stock.amnt >= amount:
        stock.amnt -= amount
        bank.cash += (amount * price)
        return True
    else:
        return False
    
#Functions for Indicators

def sma(length, dataset, ohlc):
    x = 0
    sma = []
    while x < len(dataset):
        if x < length:
            sma.append(None)
            x += 1
        else:
            i = 0
            sum = 0
            while i < length:
                if(ohlc == "Close"):
                    sum += dataset.Close[x-i]
                elif(ohlc == "Open"):
                    sum += dataset.Open[x-i]
                elif(ohlc == "High"):
                    sum += dataset.High[x-i]
                elif(ohlc == "Volume"):
                    sum += dataset.Volume[x-i]
                elif (ohlc == "ATR"):
                    sum += (dataset.High[x-i] - dataset.Low[x-i])
                else:
                    sum += dataset.Low[x-i]
                i += 1
            sum /= length
            sma.append(sum)
            x += 1
    return sma

def highLow(dataset, length):
    highLow = []
    x = 0
    while x < len(dataset):
        if x < length:
            highLow.append(None)
            x += 1
        else:
            i = 0
            flag = 1
            while i < length:
                if(dataset.High[x - i - 1] > dataset.High[x - i]):
                    flag = 0
                i += 1
            if flag == 1:
                while i < length:
                    if(dataset.Low[x - i - 1] > dataset.Low[x - i]):
                        flag = 0
                        i += 1
                if flag == 1:
                    index = 1
                    highLow.append("high")
            else:
                i = 0
                flag = 1
                while i < length:
                    if(dataset.Low[x - i - 1] < dataset.Low[x - i]):
                        flag = 0
                    i += 1
                if flag == 1:
                    index = 1
                    highLow.append("low")
                    while index <= length:
                        highLow[x - index] = "low"
                        index += 1
                else:
                    highLow.append("none")
            x += 1
    return highLow

def gapIdentify(dataset):
    gap = ["none"]
    x = 1
    while x < len(dataset):
        if (dataset['High'][x-1] < dataset['Low'][x]):
            gap.append("high")
        elif (dataset['Low'][x-1] > dataset['High'][x]):
            gap.append("low")
        else:
            gap.append("none")
        x += 1
    return gap

#Plotting Functions

def candleStickPlot(dataset):
    x = 0
    while x < len(dataset):
        for i in range(31):
            xval = dataset.index[x] + timedelta(minutes = (i - 15))
            if i >= 13 and i <= 17:
                plt.vlines(x = xval, ymin = dataset['Low'][x], ymax = dataset['High'][x], color = 'black', linewidth = 1)
    
            if dataset['Open'][x] < dataset['Close'][x]:
                priceRange = dataset['Close'][x] - dataset['Open'][x]
                xval = dataset.index[x] + timedelta(minutes = (i - 15))
                if i == 0 or i == 30:
                    plt.vlines(x = xval, ymin = dataset['Open'][x], ymax = dataset['Close'][x], color = 'black', linewidth = 1)
                else:
                    plt.vlines(x = xval, ymin = dataset['Open'][x], ymax = dataset['Open'][x] + 0.02*priceRange, color = 'black', linewidth = 1)
                    plt.vlines(x = xval, ymin = dataset['Close'][x] - 0.02*priceRange, ymax = dataset['Close'][x], color = 'black', linewidth = 1)
            else:
                plt.vlines(x = xval, ymin = dataset['Close'][x], ymax = dataset['Open'][x], color = 'black', linewidth = 1)  
        x += 1 

def ohlcPlot(dataset):
    x = 0
    while x < len(dataset):
        plt.vlines(x = dataset.index[x], ymin = dataset['Low'][x], ymax  = dataset['High'][x], color = 'black', linewidth = 0.5, linestyle = '--')
        dataset.plot(y = ["Close", "Open","SMA"], lw = 0.75)
        x += 1



