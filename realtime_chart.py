import pandas as pd
import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

ticker=sys.argv[1]

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

def animate(i):

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
    print(ticker,' ',str(increase_1min)[0:5],' ',str(increase_3min)[0:5],' ',str(increase_5min)[0:5],' ',str(increase_10min)[0:5])

    plt.cla()
    #plt.figure(0,figsize=(10,8))
    plt.subplot(221)
    plt.plot(time_1d,open_1d)
    #plt.plot(time_1d,close_1d)
    plt.axis([time_1d[0],time_1d[-1],min(open_1d),max(open_1d)])
    for i in range(len(ind_1d)):
        plt.plot([time_1d[ind_1d[i]],time_1d[ind_1d[i]]],[min(open_1d),max(open_1d)],'--',color='grey')
    plt.xlabel('1 Day')
    plt.ylabel('Price')
    plt.title(ticker)

    plt.subplot(222)
    plt.plot(time_5d,open_5d)
    #plt.plot(time_5d,close_5d)
    plt.axis([time_5d[0],time_5d[-1],min(open_5d),max(open_5d)])
    for i in range(len(ind_5d)):
        plt.plot([time_5d[ind_5d[i]],time_5d[ind_5d[i]]],[min(open_5d),max(open_5d)],'--',color='grey')
    plt.xlabel('5 Day')
    plt.ylabel('Price')

    plt.subplot(223)
    plt.plot(time_10d,open_10d)
    #plt.plot(time_10d,close_10d)
    plt.axis([time_10d[0],time_10d[-1],min(open_10d),max(open_10d)])
    for i in range(len(ind_10d)):
        plt.plot([time_10d[ind_10d[i]],time_10d[ind_10d[i]]],[min(open_10d),max(open_10d)],'--',color='grey')
    plt.xlabel('10 Day')
    plt.ylabel('Price')
    
    yrange=max(open_1d)-min(open_1d)
    plt.subplot(224)
    plt.plot(time_1d,open_1d)
    plt.axis([max(time_1d)-120,max(time_1d),min(open_1d),max(open_1d)])
    plt.xlabel('Now')
    plt.ylabel('Price')
    plt.text(time_1d[-1],open_1d[-1],str(open_1d.tolist()[-1]))
    if increase_1min<0.:
        color_1min='red'
    elif increase_1min>1:
        color_1min='magenta'
    else:
        color_1min='green'

    if increase_3min<0.:
        color_3min='red'
    elif increase_3min>1:
        color_3min='magenta'
    else:
        color_3min='green'

    if increase_5min<0.:
        color_5min='red'
    elif increase_5min>1:
        color_5min='magenta'
    else:
        color_5min='green'

    if increase_10min<0.:
        color_10min='red'
    elif increase_10min>1:
        color_10min='magenta'
    else:
        color_10min='green'

    plt.text(time_1d[-1]-30,open_1d[-1]-yrange*0.1,'1min increase='+str(increase_1min)[0:5]+'%',color=color_1min)
    plt.text(time_1d[-1]-30,open_1d[-1]-yrange*0.2,'3min increase='+str(increase_3min)[0:5]+'%',color=color_3min)
    plt.text(time_1d[-1]-30,open_1d[-1]-yrange*0.3,'5min increase='+str(increase_5min)[0:5]+'%',color=color_5min)
    plt.text(time_1d[-1]-30,open_1d[-1]-yrange*0.4,'10min increase='+str(increase_10min)[0:5]+'%',color=color_10min)

    
    print(open_1d.tolist()[-1])
ani = FuncAnimation(plt.gcf(),animate,blit=False,interval=10000)
plt.tight_layout()
plt.show()



