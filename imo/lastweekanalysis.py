#!/usr/bin/bash

import pandas as pd
import numpy as np
import sys
import time
import datetime as dt
import matplotlib.pyplot as plt

data = pd.read_csv('route32_20150904.csv').dropna()



lat, lon = 43.704248, -79.410376
lat2, lon2 = 43.6590286,-79.3714437


def searchBtwn(df, lat1,lat2, lon1,lon2):
	return df[(np.abs(data['binlat'] - lat1) < 0.001) & (np.abs(data['binlon'] - lon1) < 0.001)]


data_select =  searchBtwn(data,lat,lat2,lon,lon2)
print data_select

def timeSelect(df,timeS):
	return df[(df['bintime']/3600 == timeS)]

std = []
avg = []
for i in range(0,50):
	avg.append((timeSelect(data_select,float(i)/2)['mean'].values).mean()*3.6)
	std.append(timeSelect(data_select,float(i)/2)['std'].values.mean()*3.6)
timebins = np.linspace(0,24,50)
print timeSelect(data_select,float(i)/2)['mean']
# print timebins


# print timeSelect(data_select,9.0)

# print data_select['bintime']/3600
plt.figure()
plt.plot(timebins, avg,'ro', label = "Mean Speed")
plt.plot(timebins, std,'ko', label = "Variance")
plt.legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2)
plt.xlim(0,24)
plt.title('Englinton Construction 09-04 North')
plt.savefig('meanvar_englinton_0904.png')

plt.figure()
plt.plot(timebins, np.divide(std,avg),'ko', label = "Unreliability")
plt.title('Englinton Construction 09-04 North')
plt.xlim(0,24)
plt.legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2)
plt.savefig('unreliability_englinton_0904.png')
