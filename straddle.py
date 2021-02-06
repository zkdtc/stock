# https://www.geeksforgeeks.org/get-post-requests-using-python/
# importing the requests library 
import requests 
import datetime
import matplotlib.pyplot as plt
import numpy as np
symbols=["QQQ","AAPL","JMIA","NIO","PTON","OPEN","TSLA","U","MRNA"]
symbols=["ACB","FUBO","JMIA","QS","NIO","ARRY","OPEN","MRNA"]
def match_call_put(calls,puts,use_ask=True):
    n_calls = len(calls)
    n_puts =  len(puts)
    out_calls=[]
    out_puts=[]
    out_calls_iv=[]
    out_puts_iv=[]
    out_strike=[]
    last = 0
    for i in range(n_calls):
        strike_call = calls[i]['strike']
        for j in range(n_puts-last):
            j=j+last
            strike_put =  puts[j]['strike']
            if strike_call == strike_put:
                out_strike.append(strike_call)
                try:
                    if use_ask:#((calls[i]['ask']+calls[i]['bid'])/2.<calls[i]['lastPrice']*0.7):
                        out_calls.append(calls[i]['ask'])
                        #out_calls.append((calls[i]['ask']+calls[i]['bid'])/2.)
                    else:
                        out_calls.append(calls[i]['lastPrice'])
                except:
                    out_calls.append(calls[i]['lastPrice'])
                try:
                    if use_ask: #((puts[j]['ask']+puts[j]['bid'])/2.<puts[j]['lastPrice']*0.7):
                        out_puts.append(puts[j]['ask'])
                        #out_puts.append((puts[j]['ask']+puts[j]['bid'])/2.)
                    else:
                        out_calls.append(puts[j]['lastPrice'])
                except:
                    out_puts.append(puts[i]['lastPrice'])
                out_calls_iv.append(calls[i]['impliedVolatility'])
                out_puts_iv.append(puts[j]['impliedVolatility'])
                last = j
                break
    return np.array(out_strike), np.array(out_calls),np.array(out_calls_iv),np.array(out_puts),np.array(out_puts_iv)

def plot_one(symbol,limit=5):
    print('ploting ',symbol) 
    # api-endpoint 
    URL = "https://query2.finance.yahoo.com/v7/finance/options/"+symbol #?date=1674172800"
  
    # sending get request and saving the response as response object 
    r = requests.get(url = URL) 
  
    # extracting data in json format 
    data = r.json()
    price=data['optionChain']['result'][0]['quote']['regularMarketPrice']
    # Available contracts
    expirationDates_arr=data['optionChain']['result'][0]['expirationDates']
    plot_range = [price*0.5,price*1.5,0,price*0.3]
    n_e = min([len(expirationDates_arr),limit])
    for j in range(n_e):
        expirationDates=expirationDates_arr[j]
        r_t =  requests.get(url = URL+'?date='+str(expirationDates))
        data_t = r_t.json()
        calls = data_t['optionChain']['result'][0]['options'][0]['calls']
        puts  = data_t['optionChain']['result'][0]['options'][0]['puts']
        n = len(calls)
        strike_arr,p_call_arr,iv_call_arr,p_put_arr,iv_put_arr = match_call_put(calls,puts)
        #print(p_call_arr)
        #print(p_put_arr)
        #import pdb;pdb.set_trace()
      
        plt.plot(strike_arr,p_call_arr+p_put_arr)
        if j<2:
            ind_min=np.argmin(p_call_arr+p_put_arr)
            p_min=np.min(p_call_arr+p_put_arr)
            plt.plot([p_min,p_min],[0,price],'r--')
            plt.text(plot_range[0]+(plot_range[1]-plot_range[0])*0.15,p_min,'min='+str(p_min)[0:5]+'@'+str(strike_arr[ind_min])+' IV='+str((iv_call_arr[ind_min]+iv_put_arr[ind_min])/2.)[0:5])
        
        
        #plt.plot(strike_arr,p_call_arr+p_put_arr-np.abs(strike_arr-price))
        #plt.plot(strike_arr,p_call_arr-np.abs(strike_arr-price))
        #plt.plot(strike_arr,p_put_arr-np.abs(strike_arr-price))
    plt.plot([price,price],[0,price],'b--')
    plt.plot(np.array([-1000,0,1000])+price,[1000,0,1000],'b--')
    plt.title(symbol+' '+str(price))
    plt.axis(plot_range)

fig=plt.figure(0,figsize=(10,8))

for i in range(len(symbols)):
    ax = fig.add_subplot(3,3,i+1)
    plot_one(symbols[i])
    if i == len(symbols)-1:
        ax.text(0.55,0.1,datetime.datetime.now(),transform=ax.transAxes)
plt.tight_layout()
plt.show()



 
