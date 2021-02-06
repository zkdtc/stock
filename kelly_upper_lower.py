import numpy as np
import matplotlib.pyplot as plt
p_win_arr=[0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7]
price_low=1600.0
price_high=1800.0
price_arr=price_low+(1+np.arange(9))*(price_high-price_low)/10.

n_p_win=len(p_win_arr)
n_price=len(price_arr)
f_arr=np.zeros([n_p_win,n_price])

for i in range(n_p_win):
    p_win=p_win_arr[i]
    for j in range(n_price):
        price=price_arr[j]
        f_arr[i,j]=p_win*price/(price-price_low)-(1-p_win)*price/(price_high-price)

f_arr=100*f_arr/np.max(f_arr)
print(f_arr.astype(int))
print(p_win_arr)
print(price_arr)

