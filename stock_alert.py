import pandas as pd
import sys
import time
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import smtplib, ssl

"""
stockBot
A smart robot helps you finding realtime buying/selling oppotunities. 
Input: 
    ticker
    range: the buying/selling price you want to set

"""


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

ticker_arr=['AAPL','TSLA','NIO']
alert_range=[[394.5,400],[1479,1700],[9.35,13.65]]
plot=True #False
if len(ticker_arr)>16:
    print('Can not handle more than 16 stocks')
    sys.exit()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    UP = '\033[92m'
    T = '\033[93m' # brown yellow
    DOWN = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def shape_fit(x):
    ind=np.where(x==min(x))
    if ind[0][0]==0:
        i1=0.
        i2=100.*(x[-1]-x[0])/x[0]
    elif ind[0][0]==len(x)-1:
        i1=100.*(x[-1]-x[0])/x[0]
        i2=0.
    else:
        i1=100.*(x[ind[0][0]]-x[0])/x[0]
        i2=100.*(x[-1]-x[ind[0][0]])/x[ind[0][0]]
    return i1,i2

def remove_gap(x):
    diff=x-x.shift(1,fill_value=min(x))
    x_arr=np.array(x.tolist())
    diff=np.array(diff.tolist())
    ind=np.where(diff >300)
    n=len(ind[0])
    for i in range(n):
        x_arr[ind[0][i]:]=x_arr[ind[0][i]:]-diff[ind[0][i]]+np.median(diff)
    #print(x_arr-np.roll(x_arr,1)) 
    #x_arr=x_arr-x_arr[-1]
    return x_arr,ind[0]

def handle_one_stock(ticker,index,range):

    my_share=share.Share(ticker)
    symbol_data=None
    try:
        symbol_data_1d=my_share.get_historical(share.PERIOD_TYPE_DAY,1,share.FREQUENCY_TYPE_MINUTE,1)
        symbol_data_5d=my_share.get_historical(share.PERIOD_TYPE_DAY,5,share.FREQUENCY_TYPE_MINUTE,5)
        symbol_data_10d=my_share.get_historical(share.PERIOD_TYPE_DAY,10,share.FREQUENCY_TYPE_MINUTE,15)
        ### Convert from ms to min ###
        time_1d=pd.Series(symbol_data_1d['timestamp'])/60000.
        time_5d=pd.Series(symbol_data_5d['timestamp'])/60000.
        time_10d=pd.Series(symbol_data_10d['timestamp'])/60000.
        time_1d,ind_1d=remove_gap(time_1d)
        time_5d,ind_5d=remove_gap(time_5d)
        time_10d,ind_10d=remove_gap(time_10d)
        #import pdb;pdb.set_trace()
        open_1d=pd.Series(symbol_data_1d['open'])
        open_1d=open_1d.fillna(method='ffill')
        open_1d=open_1d.interpolate(method='nearest')
        open_5d=pd.Series(symbol_data_5d['open'])
        open_5d=open_5d.interpolate(method='nearest')
        open_10d=pd.Series(symbol_data_10d['open'])
        open_10d=open_10d.interpolate(method='nearest')

        close_1d=pd.Series(symbol_data_1d['close'])
        close_1d.interpolate(method='nearest')
        close_5d=pd.Series(symbol_data_5d['close'])
        close_5d.interpolate(method='nearest')
        close_10d=pd.Series(symbol_data_10d['close'])
        close_10d.interpolate(method='nearest')
       
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)
    open_1d=np.array(open_1d.tolist())
    open_5d=np.array(open_5d.tolist())
    open_10d=np.array(open_10d.tolist())
    close_1d=np.array(close_1d.tolist())
    close_5d=np.array(close_5d.tolist())
    close_10d=np.array(close_10d.tolist())
    
    current_price=open_1d[-1]
    print(ticker,' ',range[0],' ',f"{bcolors.HEADER}"+str(current_price)+f"{bcolors.ENDC}",' ',range[1])
    ######## stockBot thinks here ############
    interval=range[1]-range[0]
    alert_margin=0.1*interval
    
    if ((range[1]-current_price)<=alert_margin or (current_price-range[0])<=alert_margin ):
        print(ticker,' ',f"{bcolors.DOWN}"+str(current_price)+" very close to buying/selling oppotunity!"+f"{bcolors.ENDC}",' ',range[1]) 
        sys.stdout.write('\a')
        sys.stdout.flush()
 
    ######## Plot ###########
    if (plot):
        
        yrange=max(open_1d)-min(open_1d)
        cmd='plt.subplot(3,1,'+str(index+1)+')'
        a=exec(cmd)

        num_bins=100 # precission    
        plt.hist(open_10d, num_bins, range=(range[0],range[1]), normed=1, color='yellow',label='10d')
        plt.hist(open_5d, num_bins, range=(range[0],range[1]), normed=1, color='blue',label='5d')
        plt.hist(open_1d, num_bins, range=(range[0],range[1]), normed=1, color='green',label='1d')  
        plt.plot([current_price,current_price],[0,10],'b-')
        plt.xlabel('Price')
        plt.ylabel('N')
 
        plt.axis([range[0],range[1],0,1])  # set ploting range
        plt.title(ticker+' '+str(current_price))
        plt.legend(loc=0)

def animate(i):
     
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Ticker'+'    buy    current    sell\n')
    for i in range(len(ticker_arr)):
        ticker=ticker_arr[i]
        handle_one_stock(ticker,i,alert_range[i])

#ani = FuncAnimation(plt.gcf(),animate,blit=False,interval=30000)
while True:
    animate(0)
    plt.show()
    time.sleep(30)

