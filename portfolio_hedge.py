import pandas as pd
import sys
import time
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import smtplib, ssl



""" Sending email function disabled for now 
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "zkdtckk.python@gmail.com"  # Enter your address
receiver_email = "zkdtckk@gmail.com"  # Enter receiver address
password = input("Type your password and press enter: ")
context = ssl.create_default_context()

#with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message)
"""

ticker_arr=['QQQ','VOO','QTEC','MCHI',  'TECS','YANG']
ticker_arr=['QQQ','YANG']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    UP = '\033[92m'
    T = '\033[93m' # brown yellow
    DOWN = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def handle_one_stock(ticker,index):

    my_share=share.Share(ticker)
    symbol_data=None
    try:
        symbol_data_1y=my_share.get_historical(share.PERIOD_TYPE_YEAR,1,share.FREQUENCY_TYPE_DAY,1)
        symbol_data_2y=my_share.get_historical(share.PERIOD_TYPE_YEAR,2,share.FREQUENCY_TYPE_DAY,1)
        symbol_data_5y=my_share.get_historical(share.PERIOD_TYPE_YEAR,5,share.FREQUENCY_TYPE_DAY,1)
        ### Convert from ms to min ###
        time_1y=pd.Series(symbol_data_1y['timestamp'])
        time_2y=pd.Series(symbol_data_2y['timestamp'])
        time_5y=pd.Series(symbol_data_5y['timestamp'])
        open_1y=pd.Series(symbol_data_1y['open'])
        open_1y=open_1y.fillna(method='ffill')
        open_1y=open_1y.interpolate(method='nearest')
        open_2y=pd.Series(symbol_data_2y['open'])
        open_2y=open_2y.fillna(method='ffill')
        open_2y=open_2y.interpolate(method='nearest')
        open_5y=pd.Series(symbol_data_5y['open'])
        open_5y=open_5y.fillna(method='ffill')
        open_5y=open_5y.interpolate(method='nearest')

        close_1y=pd.Series(symbol_data_1y['close'])
        close_1y=open_1y.fillna(method='ffill')
        close_1y=open_1y.interpolate(method='nearest')
        close_2y=pd.Series(symbol_data_2y['close'])
        close_2y=open_2y.fillna(method='ffill')
        close_2y=open_2y.interpolate(method='nearest')
        close_5y=pd.Series(symbol_data_5y['close'])
        close_5y=open_5y.fillna(method='ffill')
        close_5y=open_5y.interpolate(method='nearest')
 
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)
    open_1y=np.array(open_1y.tolist())
    open_2y=np.array(open_2y.tolist())
    open_5y=np.array(open_5y.tolist())
    close_1y=np.array(close_1y.tolist())
    close_2y=np.array(close_2y.tolist())
    close_5y=np.array(close_5y.tolist())

    output={'time_1y':(time_1y-time_1y[0])/31190400000.*364,'time_2y':(time_2y-time_2y[0])/31190400000.*364,'time_5y':(time_5y-time_5y[0])/31190400000.*364,'open_1y':open_1y/open_1y[0],'open_2y':open_2y/open_2y[0],'open_5y':open_5y/open_5y[0],'close_1y':close_1y/close_1y[0],'close_2y':close_2y/close_2y[0],'close_5y':close_5y/close_5y[0]}

    return output

d0=handle_one_stock(ticker_arr[0],0)
for i in range(len(ticker_arr)):
    ticker=ticker_arr[i]
    cmd='d'+str(i)+'=handle_one_stock(ticker_arr['+str(i)+'],i)'
    a=exec(cmd)


plt.cla()
plt.figure(0,figsize=(10,8))
plt.subplot(3,1,1)
plt.plot(d0['time_1y'],d0['open_1y'])
plt.xlabel('1 Year')
plt.ylabel('Price')
plt.title(ticker_arr[0])

plt.subplot(3,1,2)
plt.plot(d1['time_1y'],d1['open_1y'])
plt.xlabel('1 Year')
plt.ylabel('Price')
plt.title(ticker_arr[1])

plt.subplot(3,1,3)
plt.plot(d0['time_1y'],d0['open_1y']+d1['open_1y']/3.)
plt.xlabel('1 Year')
plt.ylabel('Price')
plt.title(ticker_arr[0]+'+'+ticker_arr[1])

plt.show()







    
