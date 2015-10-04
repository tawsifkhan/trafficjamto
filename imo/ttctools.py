#!/usr/bin/bash

import pandas as pd
import numpy as np
import sys
import time
import datetime as dt
import matplotlib.pyplot as plt

route = int(sys.argv[1])
time_bin = 0.5*3600
dist_bin = 50



# data=pd.read_csv(sys.argv[1], usecols=['hmsID','secSince','vehicleID','routeID','lat','lon','heading'], dtype={'hmsID':object})

def convertHMS(value):
    temp = time.strptime(value, "%H%M%S")
    return dt.timedelta(hours=temp.tm_hour,minutes=temp.tm_min, seconds=temp.tm_sec).seconds

def convertHMSloop(df):
    for i in range(0,41):
        df[i*100000:(i+1)*100000] = df[i*100000:(i+1)*100000].apply(convertHMS)

def searchradius(df, lat,latrad, lon,lonrad):
	return df[(np.abs(df['lat']-lat)<+latrad) & (np.abs(df['lon']-lon<lonrad))]


data = pd.read_csv("20140911.csv.speed.csv").dropna()
data = data[(data['speed']>0.5) & (data['y']<0) & (data['x']<0)]

def stream():
	rtminy = data[(data['routeTag'] == route)]['y'].min()
	rtmaxy = data[(data['routeTag'] == route)]['y'].max()
	rtminx = data[(data['routeTag'] == route)]['x'].min()
	rtmaxx = data[(data['routeTag'] == route)]['x'].max()
	if np.abs(rtminy-rtmaxy) > np.abs(rtminx-rtmaxx):
		rtmin = rtminy
		rtmax = rtmaxy
		stream = 'y'
	else:
		rtmin = rtminx
		rtmax = rtmaxx
		stream = 'x'
	return stream,rtmin,rtmax

def func(route, hour, frac,rtmin,rtmax,stream):
	temp = data[(data['routeTag'] == route) & (np.abs(data['time'] - hour*3600.)<time_bin.) & (np.abs(data[stream] - (rtmin+rtmax)*frac) < dist_bin)]['speed']
	avg = temp.mean()
	std = temp.std()
	return avg, std, temp

stream,rtmin,rtmax = stream()
data = data[data[stream] > rtmin]
data = data[data[stream] > rtmin]
print "Route Number %r going in %s direction " % (route,stream)

times = [8,10,12,14,16,18]
avg50 = np.zeros(len(times))
std50 = np.zeros(len(times))
avg25 = np.zeros(len(times))
std25 = np.zeros(len(times))
avg75 = np.zeros(len(times))
std75 = np.zeros(len(times))

count = 0
for tt in times:
	avg25[count],std25[count],temp = func(route,tt,0.25,rtmin,rtmax,stream)
	avg50[count],std50[count],temp = func(route,tt,0.50,rtmin,rtmax,stream)
	avg75[count],std75[count],temp = func(route,tt,0.75,rtmin,rtmax,stream)
	count = count + 1

print "Times"
print times
print "Averages"
print "25\%: " , avg25
print "50\%: " , avg50
print "75\%: " , avg75

print "Variance"
print "25\%: " , std25
print "50\%: " , std50
print "75\%: " , std75

print "Reliability"
print "25\%: " , avg25/std25
print "50\%: " , avg50/std50
print "75\%: " , avg75/std75


# # plt.hist(data8.values,bins=range(0,11,1), alpha = 0.25)
