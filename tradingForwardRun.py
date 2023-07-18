#finance functions libraries
import yfinance as yf
from tradingFuncs import *
#date libraries
from datetime import datetime, date, timedelta, time
import pandas_market_calendars as mcal
#data management libraries
import pandas as pd
from twilio.rest import Client

account_sid = 'AC7040be2b9ea9589a094ea8bb6c1dc984'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

def tradeStrat(historical, SMA10, SMA5, flag):
    if historical[SMA5][len(historical) - 1] > historical[SMA10][len(historical) - 1]:
        if flag == 0:
            message = client.messages.create(
                from_='+18666741041',
                body='buy',
                to='+19736928485'
            )
            flag = 1
    if historical[SMA5][len(historical) - 1] < historical[SMA10][len(historical) - 1]:
        if flag == 1:
            message = client.messages.create(
                from_='+18666741041',
                body='sell',
                to='+19736928485'
            )
            flag = 0

stock = yf.Ticker("aapl")
today = date.today()
startDate = today - timedelta(months=2)

historical = stock.history(start=startDate, interval="1h")
historical['SMA10'] = sma(10, historical, "Close")
historical['SMA5'] = sma(5, historical, "Close")

nyse = mcal.get_calendar('NYSE')
early = nyse.schedule(start_date=startDate, end_date=today)

flag = 0
if today in early:
    while datetime.now().time() >= time(9,30) and datetime.now().time() <= time(4,00):
        tradeStrat(historical, 'SMA10', 'SMA5', flag)
        time.sleep(3600)
