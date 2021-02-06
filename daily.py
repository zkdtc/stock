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
## ~~~~~~~~~~ 03/20 ~~~~~~~~
q_1=194+2+1+4-1+4+1+2+2+15+2+2+1+1-2+2-1-2-2+2+2-2-10
q_2=289-2-1-1-3-2-21-2-1-1-1+1+1+2-1-2+2+9
cash_1=11701.83-2*51.4-2*50.59-50.6767-50.31+50.72*2-2*49.5+50.1455+50.9+51.8*2-2*50.6-2*49.5+2*51+10*55.3                       #11483.01-2*57.86-57.27-4*55.05+56-4*53.7-52.82-2*51.966-2*50.9-2*51.4-2*50.59-50.6767  # sdow
cash_2=11729.06+46.0505*2+46.031+46.5+47.47-46.7-46.28-45.3*2+46.2+2*46.6-2*45.685-9*42.91                      #12199.3+2*43+43+43.62+3*44.52+45.08*2+46.0505*2+46.031  # tqqq

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
    total_1=cash_1+stock_1
    total_2=cash_2+stock_2
    total=total_1+total_2
    buy_1=int(0.5*(cash_1-stock_1)/price_1)
    buy_2=int(0.5*(cash_2-stock_2)/price_2)
    rebalance_buy_1=int(0.25*total/price_1)-q_1
    rebalance_buy_2=int(0.25*total/price_2)-q_2
    rebalance_cash_1=0.5*total-(rebalance_buy_1+q_1)*price_1
    rebalance_cash_2=0.5*total-(rebalance_buy_2+q_2)*price_2

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





