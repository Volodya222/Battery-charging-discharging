import scipy.interpolate
from scipy import optimize
from scipy.optimize import root
import math
#from Discharge import time_to_sec

def time_to_sec(st):
    st= str(st)
    st_arr = st.split(":")

    "print(st_arr)"
    for i in range (len(st_arr)):
        st_arr[i] = int(st_arr[i])
    return st_arr[0]*3600 + st_arr[1]*60 + st_arr[2]

dis_time_10 = time_to_sec('18:46:11') - time_to_sec('14:55:8')
dis_time_15 = time_to_sec('18:36:42') - time_to_sec('16:12:23')
dis_time_20 = time_to_sec('14:42:05') - time_to_sec('12:52:13')
dis_time_17_5 = time_to_sec('18:12:33') - time_to_sec('16:00:56')
dis_time_12_5 = time_to_sec('18:44:02')-time_to_sec('15:33:51')
dis_time_25 = time_to_sec('16:13:12') - time_to_sec('14:47:40')
dis_time_35 = time_to_sec('11:52:19') - time_to_sec('10:51:40')
dis_time_30 = time_to_sec('15:06:45') - time_to_sec('13:58:31')
dis_time_40 = time_to_sec('16:10:33')-time_to_sec('15:20:46')
dis_time_test  = time_to_sec('14:21:51') - time_to_sec('13:04:51')
print(dis_time_10)
print(dis_time_12_5)
print(dis_time_15)
print(dis_time_17_5)
print(dis_time_20)
print(dis_time_25)
print(dis_time_30)
print(dis_time_35)
print(dis_time_40)
print(dis_time_test)

x7n = [dis_time_10, dis_time_12_5,dis_time_15, dis_time_17_5,dis_time_20,dis_time_30, dis_time_40]
y7n = [10, 12.5, 15, 17.5, 20, 30, 40]

x6n = [dis_time_10, dis_time_12_5,dis_time_15, dis_time_17_5,dis_time_20, dis_time_40]
y6n = [10, 12.5, 15, 17.5, 20, 41.387]

x5n = [dis_time_10, dis_time_12_5,dis_time_15, dis_time_17_5,dis_time_20]
y5n=[10, 12.5, 15, 17.5, 20]

x4n = [dis_time_10, dis_time_12_5, dis_time_17_5,dis_time_20]
y4n=[10, 12.5, 17.5, 20]

x3n = [dis_time_20, dis_time_25,dis_time_30]
y3n=[20, 25, 30]

x2n = [dis_time_10,dis_time_20]
y2n=[10, 20]

x_20_to_40 = [dis_time_20, dis_time_25, dis_time_30]
y_20_to_40 = [20, 25, 30]
x_10_to_15 = [dis_time_10, dis_time_12_5, dis_time_15]
y_10_to_15 = [10,12.5,15]


L7 = scipy.interpolate.lagrange(x7n,y7n)
L6 = scipy.interpolate.lagrange(x6n,y6n)
L5 = scipy.interpolate.lagrange(x5n,y5n)
L4 = scipy.interpolate.lagrange(x4n,y4n)
L3 = scipy.interpolate.lagrange(x3n,y3n)
L2 = scipy.interpolate.lagrange(x2n,y2n)
L_20_to_40 = scipy.interpolate.lagrange(x_20_to_40, y_20_to_40)
L_10_to_15 = scipy.interpolate.lagrange(x_10_to_15, y_10_to_15)


print(L3)
print(type(L3))
I_disch = 35

def f_L4(x):
    return (-3.696*10**(-11)*x**3 + 1.276*10**(-6)*x**2 - 0.0154*x + 76.61-15)

def f_L5(x,a):
    return(-5.417e-14*x**4 + 2.149e-09*x**3 - 3.1e-05*x**2 + 0.191*x - 405.3 - a)

def f_L6(x,a):
    return(-1.059e-17*x**5 + 4.584e-13*x**4 - 7.598e-09*x**3 + 6.003e-05*x**2 - 0.2269*x + 349.5 - a)

def f_7(x):
    return scipy.interpolate.lagrange(x6n,y6n)


#sol5 = optimize.root_scalar(f_L5, args = (I_disch), bracket = [6000, 20000],method='brentq')
#print(sol5.root)

L3 = L3 - 25
print(L3.r.min())
'''sol7 = optimize.root_scalar(f_7, bracket = [-1000, 20000],method='brentq')
print(sol7.root)'''
