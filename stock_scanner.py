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

ticker_arr=['ADAP','AREC','AHPI','FCEL','INO','MREO','MRNA','NH','NK','NTRP','NVAX','PLG','SEAC','SNCA','TNDM','XLRN']
ticker_arr=['QQQ','MCHI','BABA','BILI','JD','AKCA','APLS','APLT','BYND','LK','NIO','NVDA','PALL','SAVA','TSLA']
ticker_arr=['QQQ','VOO','QTEC','MCHI',  'TECS','SPXS','YANG','TSLA','BILI','NIO','SAVA','AMZN','UBER','LYFT','BYND','GILD']
ticker_arr=['AAPL','BILI','ZM']

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

def handle_one_stock(ticker,index):

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

    increase_1min=100.*(open_1d[-1]-open_1d[-2])/open_1d[-2]
    increase_3min=100.*(open_1d[-1]-open_1d[-4])/open_1d[-4]
    increase_5min=100.*(open_1d[-1]-open_1d[-6])/open_1d[-6]
    increase_10min=100.*(open_1d[-1]-open_1d[-11])/open_1d[-11]

    i1_10min,i2_10min=shape_fit(open_1d[-11:])
    i1_20min,i2_20min=shape_fit(open_1d[-21:])
    i1_30min,i2_30min=shape_fit(open_1d[-31:])
    i1_60min,i2_60min=shape_fit(open_1d[-61:])

    print(ticker,' ',str(i1_10min)[0:5],' ',str(i2_10min)[0:5],' ',str(i1_20min)[0:5],' ',str(i2_20min)[0:5],' ',str(i1_30min)[0:5],' ',str(i2_30min)[0:5])
    if i2_10min>=2 or i2_20min>=2 or i2_30min>=2:
        print(f"{bcolors.HEADER}ALARM!"+" "+ticker+" UP!"+f"{bcolors.ENDC}")
    ######## iStock thinks here ############
    print(ticker,' ',str(increase_1min)[0:5],' ',str(increase_3min)[0:5],' ',str(increase_5min)[0:5],' ',str(increase_10min)[0:5])
    if increase_1min>=0.5:
        print(f"{bcolors.UP}ALARM!"+" "+ticker+" increases from "+str(open_1d[-2])+" to "+str(open_1d[-1])+" in 1 min!"+f"{bcolors.ENDC}")
    if increase_3min>=0.5:
        print(f"{bcolors.UP}ALARM!"+" "+ticker+" increases from "+str(open_1d[-4])+" to "+str(open_1d[-1])+" in 3 min!"+f"{bcolors.ENDC}") 
    if increase_5min>=0.5:
        print(f"{bcolors.UP}ALARM!"+" "+ticker+" increases from "+str(open_1d[-6])+" to "+str(open_1d[-1])+" in 5 min!"+f"{bcolors.ENDC}")
    if increase_10min>=1:
        print(f"{bcolors.UP}ALARM!"+" "+ticker+" increases from "+str(open_1d[-11])+" to "+str(open_1d[-1])+" in 10 min!"+f"{bcolors.ENDC}")

    if increase_1min<=-0.5:
        print(f"{bcolors.DOWN}ALARM!"+" "+ticker+" decreases from "+str(open_1d[-2])+" to "+str(open_1d[-1])+" in 1 min!"+f"{bcolors.ENDC}")
    if increase_3min<=-0.5:
        print(f"{bcolors.DOWN}ALARM!"+" "+ticker+" decreases from "+str(open_1d[-4])+" to "+str(open_1d[-1])+" in 3 min!"+f"{bcolors.ENDC}")
    if increase_5min<=-0.5:
        print(f"{bcolors.DOWN}ALARM!"+" "+ticker+" decreases from "+str(open_1d[-6])+" to "+str(open_1d[-1])+" in 5 min!"+f"{bcolors.ENDC}")
    if increase_10min<=-1:
        print(f"{bcolors.DOWN}ALARM!"+" "+ticker+" decreases from "+str(open_1d[-11])+" to "+str(open_1d[-1])+" in 10 min!"+f"{bcolors.ENDC}")
    yrange=max(open_1d)-min(open_1d)
    cmd='plt.subplot(4,4,'+str(index+1)+')'
    a=exec(cmd)

    plt.plot(time_1d,open_1d)
    plt.axis([max(time_1d)-120,max(time_1d),min(open_1d),max(open_1d)])
    plt.title(ticker)
    #plt.text(time_1d[-1],open_1d[-1],str(open_1d.tolist()[-1]))
def animate(i):
    
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Ticker'+'    1min    3min    5min    10min\n')
    for i in range(len(ticker_arr)):
        ticker=ticker_arr[i]
        handle_one_stock(ticker,i)

plt.figure(0,figsize=(20,10))
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 10}
plt.rc('font', **font)
ani = FuncAnimation(plt.gcf(),animate,blit=False,interval=30000)
#plt.tight_layout()
plt.show()

