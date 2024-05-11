import pandas as pd
import warnings
import scipy.interpolate
from scipy import optimize
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import math

def time_to_sec(st):
    st= str(st)
    st_arr = st.split(":")

    "print(st_arr)"
    for i in range (len(st_arr)):
        st_arr[i] = int(st_arr[i])
    return st_arr[0]*3600 + st_arr[1]*60 + st_arr[2]

df_25 = pd.read_csv('Discharge_25.csv', sep =';')
df_30 = pd.read_csv('Discharge_30.csv', sep = ';')

df_30 = df_30.loc[(df_30['dischargingCurrentA'] > 10) & (df_30['dischargingCurrentA'] < 35) &
                  (df_30['houseLoadPowerW'] >= 100) & (df_30['batteryVoltageV'] > 42.9) &
                  (df_30['houseLoadPowerW'].index < 900)].reset_index()
df_30 = df_30.drop(['index'], axis = 1)
time_0 = time_to_sec(df_30['createdAt'][0][15:24])
for i in range(df_30['houseLoadPowerW'].index.max() + 1):
    df_30['createdAt'][i] = time_to_sec(df_30['createdAt'][i][15:24]) - time_0

print(df_30)


df_25 = df_25.loc[(df_25['dischargingCurrentA'] > 10) & (df_25['batteryVoltageV'] > 42.9)
& (df_25['batteryVoltageV'].index > 650)].reset_index()
df_25 = df_25.drop(['index'], axis = 1)
time_0 = time_to_sec(df_25['createdAt'][0][15:24])
for i in range (len(df_25['createdAt'])):
    df_25['createdAt'][i] = time_to_sec(df_25['createdAt'][i][15:24]) - time_0

print(df_25)

df_20 = pd.read_csv('Discharge_20.csv', sep = ';')
df_20 = df_20.loc[(df_20['PackVoltage'].index > 2) & (df_20['PackVoltage'].index < 6568)].reset_index()
df_20 = df_20.drop(['Date', 'Cell1', 'Cell2','Cell3','Cell4','Cell5','Cell6','Cell7','Cell8','Cell9',
                    'Cell10','Cell11','Cell12',
                    'Cell13','Average Vol','MaxCell','MinCell','Remain cap','Full Charge Cap','Cycle Count',
                    'temp1',
                    'temp2','temp3','CHG Fet Status','DSG Fet Status','ProtectStatus','BalanceStatus',
                    'index'],
                   axis = 1)

time_0 = time_to_sec(df_20['time'][0])
for i in range(df_20['time'].index.max() + 1):
    df_20['time'][i] = time_to_sec(df_20['time'][i]) - time_0
    df_20['current'][i] = df_20['current'][i][1:5]
    df_20['PackVoltage'][i] = df_20['PackVoltage'][i][:-1]

df_20['current'] = df_20['current'].astype(float)

df_20['PackVoltage'] = df_20['PackVoltage'].astype(float)

print(df_20)

df_test = pd.read_csv('Discharge_test.csv', sep =';')
df_test = df_test.loc[(df_test['createdAt'].index > 26 ) & (df_test['createdAt'].index < 773) &
                      (df_test['dischargingCurrentA'] > 25)].reset_index()
df_test = df_test.drop(['index'], axis = 1)
time_0 = time_to_sec(df_test['createdAt'][0][15:24])
for i in range(df_test['houseLoadPowerW'].index.max() + 1):
    df_test['createdAt'][i] = time_to_sec(df_test['createdAt'][i][15:24]) - time_0

print(df_test)



print(df_30['createdAt'][df_30[df_30['batteryVoltageV'] == 49.8].index.max()])
print(df_25['createdAt'][df_25[df_25['batteryVoltageV'] == 49.8].index.max()])
print(df_20['time'][df_20[df_20['PackVoltage'] == 49.8].index.max()])
print(df_test['createdAt'][df_test[df_test['batteryVoltageV'] == 49.8].index.max()])
print(df_test['createdAt'][df_test['createdAt'].index.max()] - df_test['createdAt'][df_test[df_test['batteryVoltageV'] == 49.8].index.max()])

def relative_error(absolut, error):
    return abs(1 - error/absolut)

def abs_error(absolut, error):
    return abs(absolut - error)

def MQTT(C, P):
    return 3600*19.5*C/P

x3_full = [df_30['createdAt'][df_30['createdAt'].index.max()], df_25['createdAt'][df_25['createdAt'].index.max()],
           df_20['time'][df_20['PackVoltage'].index.max()]]
'''y3_full = [30, 25, 20]
L3_full = scipy.interpolate.lagrange(x3_full, y3_full)
I_test = 27
L3_full -= I_test
dis_time_full = L3_full.r.min()
print(dis_time_full)'''
Voltage = []
relative_error_Lagrange = []
relative_error_MQTT = []
absolut_error_MQTT = []
absolut_error_Lagrange = []
dis_time_Lagrange_mass = []
dis_time_MQTT_mass = []
dis_time_test_mass = []
charge_lagrange = []
charge_inverner = []
#flag = df_30['batteryVoltageV'][0]
flag = 52.3
charge_percent_lagrange_0 = 100
print(type(flag))
while flag > 43.1:
    flag -= 0.1
    flag = round(flag, 1)
    print(type(flag))
    print(flag)
    if df_30['batteryVoltageV'].isin([flag]).any() & df_20['PackVoltage'].isin([flag]).any() & \
        df_25['batteryVoltageV'].isin([flag]).any() & df_test['batteryVoltageV'].isin([flag]).any():
        time_30 = df_30['createdAt'][df_30[df_30['batteryVoltageV'] == flag].index.max()]
        time_25 = df_25['createdAt'][df_25[df_25['batteryVoltageV'] == flag].index.max()]
        time_20 = df_20['time'][df_20[df_20['PackVoltage'] == flag].index.max()]
        time_test = df_test['createdAt'][df_test[df_test['batteryVoltageV'] == flag].index.max()]
        dis_time_test = df_test['createdAt'][df_test['createdAt'].index.max()] - \
                        df_test['createdAt'][df_test[df_test['batteryVoltageV'] == flag].index.max()]
        Voltage.append(flag)
        I_test = df_test['dischargingCurrentA'][df_test[df_test['batteryVoltageV'] == flag].index.max()]
        x3n = [time_20, time_25, time_30]
        y3n = [20, 25, 30]
        L3 = scipy.interpolate.lagrange(x3n, y3n)
        L3 = L3 - I_test
        roots = L3.r
        y3_full = [30, 25, 20]
        L3_full = scipy.interpolate.lagrange(x3_full, y3_full)
        L3_full -= I_test
        dis_time_full = L3_full.r.min()
        print(roots)
        time_MQTT = MQTT(df_test['chargeLevelPercent'][df_test[df_test['batteryVoltageV'] == flag].index.max()],
                         df_test['houseLoadPowerW'][df_test[df_test['batteryVoltageV'] == flag].index.max()])

        relative_error_MQTT.append(relative_error(dis_time_test, time_MQTT))
        dis_time_Lagrange = dis_time_full - roots.min()
        charge_percent_lagrange = dis_time_Lagrange*100/dis_time_full
        if charge_percent_lagrange < charge_percent_lagrange_0:
            charge_lagrange.append(charge_percent_lagrange)
            charge_percent_lagrange_0 = charge_percent_lagrange
        else:
            charge_lagrange.append(charge_percent_lagrange_0)
        charge_inverner.append(df_test['chargeLevelPercent'][df_test[df_test['batteryVoltageV'] == flag].index.max()])
        relative_error_Lagrange.append(relative_error(dis_time_test, dis_time_Lagrange))
        absolut_error_MQTT.append(abs_error(dis_time_test, time_MQTT))
        absolut_error_Lagrange.append(abs_error(dis_time_test, dis_time_Lagrange))
        dis_time_MQTT_mass.append(time_MQTT)
        dis_time_Lagrange_mass.append(dis_time_Lagrange)
        dis_time_test_mass.append(dis_time_test)
    else: a = 0

print(Voltage)
print(absolut_error_Lagrange)
print(len(Voltage))
print(len(relative_error_MQTT))


plt.semilogy(Voltage, relative_error_MQTT, "-r", label = "формула MQTT")
plt.xlabel("Напряжение")
plt.ylabel("Относительная погрешность")
plt.semilogy(Voltage, relative_error_Lagrange, "-g", label = "интерполяция")
plt.xlabel("Напряжение")
plt.ylabel("Относительная погрешность")
plt.legend()
plt.show()


plt.semilogy(Voltage, absolut_error_MQTT, "-r", label = "формула MQTT")
plt.xlabel("Напряжение")
plt.ylabel("Абсолютная погрешность")
plt.semilogy(Voltage, absolut_error_Lagrange, "-g", label = "интерполяция")
plt.xlabel("Напряжение")
plt.ylabel("Абсолютная погрешность")
plt.legend()
plt.show()

plt.semilogy(Voltage, dis_time_test_mass, label="Точное время")
plt.semilogy(Voltage, dis_time_Lagrange_mass, label="интерполяция")
plt.semilogy(Voltage, dis_time_MQTT_mass, label="MQTT")
plt.xlabel("Напряжение")
plt.ylabel("Время до разрядки")
plt.legend()
plt.show()

plt.plot(Voltage, charge_lagrange, label = 'интерполяция')
plt.plot(Voltage, charge_inverner, label = 'инвертер')
plt.xlabel("Напряжение")
plt.ylabel("Процент заряда")
plt.legend()
plt.show()