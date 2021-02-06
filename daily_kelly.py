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

data_arr=[{'ticker':'TSLA','q':0,'cost':0,'cash':30000,'buy_price':[1375,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]},\
      {'ticker':'AAPL','q':0,'cost':0,'cash':40000,'buy_price':[1375,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]}, \
      {'ticker':'BAC','q':0,'cost':0,'cash':20000,'buy_price':[1375,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]}, \
      {'ticker':'MRNA','q':0,'cost':0,'cash':10000,'buy_price':[1375,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]}, \
      {'ticker':'SLV','q':0,'cost':0,'cash':6000,'buy_price':[20,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]}, \
      {'ticker':'GLD','q':0,'cost':0,'cash':4000,'buy_price':[1375,1500,1550],'buy_ratio':[0.4,0.25,0.1],'sell_price':[1630,1670,1750],'sell_ratio':[0.1,0.25,0.4]}]


## Email alert thresholds 
sent=False

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "zkdtckk.python@gmail.com"  # Enter your address
receiver_email = "zkdtckk@gmail.com"  # Enter receiver address
password = "zhangkaizhengdaqian" #input("Type your password and press enter: ")
context = ssl.create_default_context()

while True:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for data in data_arr:
        ### Get Price ###
        ticker=data['ticker']
        q=data['q']
        cash=data['cash']
        buy_price=data['buy_price']
        buy_ratio=data['buy_ratio']
        sell_price=data['sell_price']
        sell_ratio=data['sell_ratio']
        
        try:
            my_share=share.Share(ticker)
            symbol_data=None
            symbol_data_1d=my_share.get_historical(share.PERIOD_TYPE_DAY,1,share.FREQUENCY_TYPE_MINUTE,1)
        

            price=symbol_data_1d['close'][-1]
            if not price:
                price=0.
        except:
            price=float(input('Input price for '+ticker+':'))


        stock=q*price
        total=cash+stock
        buy5=cash*buy_ratio[0]/price
        buy3=cash*buy_ratio[1]/price
        buy1=cash*buy_ratio[2]/price

        sell1=q*sell_ratio[0]
        sell3=q*sell_ratio[1]
        sell5=q*sell_ratio[2]

        print(ticker,'quantity:',int(q),'stock:',decimal.Decimal("%.2f" % stock),'   cash:',decimal.Decimal("%.2f" % cash),'   Total:',decimal.Decimal("%.2f" % total),'  Price:',str(price)[0:5])
        print('Buy ladder: ',buy_price, ' 5:',int(buy5), ' 3:',int(buy3), ' 1:',int(buy1))
        print('Sell ladder: ',sell_price, ' 5:',int(sell5), ' 3:',int(sell3), ' 1:',int(sell1))
    
        if (np.abs(price)<=buy1 or np.abs(sell1)>=1):
            sys.stdout.write('\a')
            sys.stdout.flush()
        """
        message='adjust buy_1:'+str(buy_1)+'  buy_2:'+str(buy_1)
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        sent=True
        """
    time.sleep(30)





