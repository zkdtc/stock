import pandas as pd
import sys
import time
import decimal
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import smtplib, ssl

ticker_1='sdow'
ticker_2='tqqq'
q1=10
q2=10
price_in_1=0
price_in_2=0

## ~~~~~~~~~~ 03/20 ~~~~~~~~
## Email alert thresholds 
sent=False
thres_1=5
thres_2=5

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "zkdtckk.python@gmail.com"  # Enter your address
receiver_email = "zkdtckk@gmail.com"  # Enter receiver address
password = "zhangkaizhengdaqian" #input("Type your password and press enter: ")
context = ssl.create_default_context()

while True:
    ### Get Price ###
    try:
        my_share_1=share.Share(ticker_1)
        my_share_2=share.Share(ticker_2)
        symbol_data=None
        symbol_data_1d_1=my_share_1.get_historical(share.PERIOD_TYPE_DAY,1,share.FREQUENCY_TYPE_MINUTE,1)
        symbol_data_1d_2=my_share_2.get_historical(share.PERIOD_TYPE_DAY,1,share.FREQUENCY_TYPE_MINUTE,1)

        price_1=symbol_data_1d_1['close'][-1]
        price_2=symbol_data_1d_2['close'][-1]
        if not price_1:
            price_1=0.
        if not price_2:
            price_2=0.
    except:
        price_1=float(input('Input price_1:'))
        price_2=float(input('Input price_2:'))


    stock_1=q_1*price_1
    stock_2=q_2*price_2

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(ticker_1,'quantity:',int(q_1),'stock:',decimal.Decimal("%.2f" % stock_1),'   cash:',decimal.Decimal("%.2f" % cash_1),'   Total:',decimal.Decimal("%.2f" % total_1),'  Price:',str(price_1)[0:5],'  Buy:',buy_1)
    print(ticker_2,'quantity:',int(q_2),'stock:',decimal.Decimal("%.2f" % stock_2),'   cash:',decimal.Decimal("%.2f" % cash_2),'   Total:',decimal.Decimal("%.2f" % total_2),'  Price:',str(price_2)[0:5],'  Buy:',buy_2)
    print('Total value:',decimal.Decimal("%.2f" % total),ticker_1+'/'+ticker_2+'=',float(total_1)/float(total_2))
    print('To rebalance:')
    print(ticker_1,'Buy: ',rebalance_buy_1,' New quantity:',q_1+rebalance_buy_1,' New cash:',decimal.Decimal("%.2f" % rebalance_cash_1))
    print(ticker_2,'Buy: ',rebalance_buy_2,' New quantity:',q_2+rebalance_buy_2,' New cash:',decimal.Decimal("%.2f" % rebalance_cash_2))
    
    if (np.abs(buy_1)>=thres_1 or np.abs(buy_2)>=thres_2):
        sys.stdout.write('\a')
        sys.stdout.flush()
    """
        message='adjust buy_1:'+str(buy_1)+'  buy_2:'+str(buy_1)
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        sent=True
    """
    time.sleep(10)





