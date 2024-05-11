import pandas as pd
import scipy.interpolate
import numpy as np
import matplotlib.pyplot as plt
#df = pd.read_csv('Discharge_10Acs.csv')
df_10 = pd.read_excel('Discharge_10A.xlsx')
df_15 = pd.read_excel('Discharge_20A.xlsx')
df_20 = pd.read_excel('Discharge_20A.xlsx')

df_noV = []
for i in range (len(df_10['PackVoltage'])):
    df_10['PackVoltage'][i] = df_10['PackVoltage'][i][:-1]
print(type(df_10['PackVoltage'][3]))
#for i in range (len(df_15['PackVoltage'])):
 #   df_15['PackVoltage'][i] = df_15['PackVoltage'][i][:-1]

#for i in range (len(df_20['PackVoltage'])):
 #   df_20['PackVoltage'][i] = df_20['PackVoltage'][i][:-1]
print(float(df_10['PackVoltage'][3]))
k = 0
for i in range (len(df_10['PackVoltage'])):
    if float(df_10['PackVoltage'][i]) == 43.0:
        k = i
        break
print(df_10['time'][k])


def time_to_sec(st):
    st= str(st)
    st_arr = st.split(":")

    "print(st_arr)"
    for i in range (len(st_arr)):
        st_arr[i] = int(st_arr[i])
    return st_arr[0]*3600 + st_arr[1]*60 + st_arr[2]
def delta_time_df_10(x):
    return time_to_sec(x) - time_to_sec(df_10['time'][0])



dis_time_10 = time_to_sec('18:46:11') - time_to_sec('14:55:8')
dis_time_15 = time_to_sec('18:36:42') - time_to_sec('16:12:23')
dis_time_20 = time_to_sec('14:42:04') - time_to_sec('12:52:13')
print(dis_time_10)
print(dis_time_15)
print(dis_time_20)

xn = [dis_time_10, dis_time_15, dis_time_20]
yn=[10, 15, 20]

L = scipy.interpolate.lagrange(xn,yn)

print(L)






