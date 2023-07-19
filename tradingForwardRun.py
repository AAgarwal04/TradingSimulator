#finance functions libraries
import yfinance as yf
from tradingFuncs import *
#date libraries
from datetime import datetime, date, timedelta, time
import time
import pandas_market_calendars as mcal
#data management libraries
import pandas as pd
from twilio.rest import Client

#Fill out the following boxes with your Twilio Information
account_sid = ['Account ID']
auth_token = ['AuthToken']
twilioNumber = ['TwilioPhoneNumber']
myNumber = ['YourPhoneNumber']
client = Client(account_sid, auth_token)

def tradeStrat(stock, startDate, flag):
    historical = stock.history(start=startDate, interval="1h")
    historical['SMA10'] = sma(10, historical, "Close")
    historical['SMA5'] = sma(5, historical, "Close")
    print(historical['Close'][len(historical) - 1])
    if historical['SMA5'][len(historical) - 1] > historical['SMA10'][len(historical) - 1]:
        if flag == 0:
            message = client.messages.create(
                from_= twilioNumber,
                body='buy',
                to=myNumber
            )
            flag = 1
    if historical['SMA5'][len(historical) - 1] < historical['SMA10'][len(historical) - 1]:
        if flag == 1:
            message = client.messages.create(
                from_= twilioNumber,
                body='sell',
                to=myNumber
            )
            flag = 0

stock = yf.Ticker("aapl")
today = date.today()
startDate = today - timedelta(days=2)



nyse = mcal.get_calendar('NYSE')
early = nyse.schedule(start_date=startDate, end_date=today)

flag = 0
closedFlag = 0
while True:
    if str(today) in early.index:
        time930 = datetime.now().time().replace(hour=9, minute=30, second=0, microsecond=0)
        time400 = datetime.now().time().replace(hour = 21, minute = 0, second = 0, microsecond=0)
        if datetime.now().time() >= time930 and datetime.now().time() <= time400:
            if closedFlag == 1:
                closedFlag = 0
                message = client.messages.create(
                    from_=twilioNumber,
                    body='Market Open',
                    to=myNumber
                )
            tradeStrat(stock, startDate, flag)
            time.sleep(3600)
        else:
            if closedFlag == 0:
                message = client.messages.create(
                    from_=twilioNumber,
                    body='Market Closed',
                    to=myNumber
                )
                closedFlag = 1
            time.sleep(1800)
    else:
        time.sleep()