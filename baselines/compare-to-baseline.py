#!/usr/bin/env python

from __future__ import print_function
import pandas as pd
import numpy as np
import pyproj
import time
import argparse
import os

def timeFromHMS(hms):
    hmsint = hms.astype(np.int)
    seci = np.mod(hmsint,100)
    mini = np.mod(hmsint/100,100)
    hri = np.mod(hmsint/10000,100)
    return (hri*60+mini)*60+seci

def dataFromFile(filename, maxspeed):
    data = pd.read_csv(filename).dropna()
    if not 'time' in data.columns:
        data.columns = ['hmsID','id','route','dirTag','lat','lon','secsSinceReport','whocares','heading']
        data['time'] = timeFromHMS(data['hmsID'].values)
        data = data.drop('whocares',1)

    data['time'] = data['time'] - data['secsSinceReport']
    data = data.drop('secsSinceReport',1).drop('dirTag',1).drop('hmsID',1)
    data = data.sort(['id','time'])

    start = time.time()
    data['x'], data['y'] = proj(data['lon'].values, data['lat'].values)

    allids = data['id'].unique()
#    start = time.time()
#    for vid in allids:
#        vehicledata = data['id']==vid
#        dx = data.loc[vehicledata, 'x'].diff().values
#        dy = data.loc[vehicledata, 'y'].diff().values
#        dt = data.loc[vehicledata, 'time'].diff().values
#        dist = np.sqrt(dx*dx+dy*dy)
#        data.loc[vehicledata, 'speed'] = dist/(dt+0.1)
#        print(time.time()-start)
#        start = time.time()
#
    grouped = data.groupby('id')
    dx = grouped['x'].diff().values
    dy = grouped['y'].diff().values
    dt = grouped['time'].diff().values
    dist = np.sqrt(dx*dx+dy*dy)

    data['speed'] = dist/dt
    data.dropna()
    data = data.loc[(data.speed > 0.5) & (data.speed < maxspeed)]
    return data

def binData(data, spatialRes=200, headingRes=45, timeRes=30):
    timeRes = timeRes*60.
    data['binx'] = np.round(data['x']/spatialRes)*spatialRes
    data['biny'] = np.round(data['y']/spatialRes)*spatialRes
    data['binlon'], data['binlat'] = proj(data['x'].values, data['y'].values, inverse=True)
    data['bintime'] = (np.round(1.0*data['time'].values/timeRes).astype(np.int)*timeRes).astype(np.int)
    data['binheading'] = np.round(1.0*data['heading'].values/headingRes).astype(np.int)*headingRes
    return data

def groupData(data, minpts=5):
    grouped = data.groupby(['binlat','binlon','bintime','binheading'])
    grouped = pd.DataFrame(grouped['speed'].agg([len, np.mean, np.std]))
    grouped = grouped.loc[grouped.len > 5]
    return grouped

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('baseline', help="Raw input csv files of baseline")
    parser.add_argument('day', help="Raw input csv files")
    parser.add_argument('route',type=int, help="Route number")
    parser.add_argument('hourstart',type=float, help="starting hour")
    parser.add_argument('hourend',type=float, help="starting hour")
    parser.add_argument('-o','--output', type=str, default="grouped.csv", help="Output file name")
    args = parser.parse_args()

    proj = pyproj.Proj("+proj=utm +zone=17N, +ellps=WGS84 +datum=WGS84 +units=m +no_defs")


    print('reading day data')
    daydata = dataFromFile(args.day, 15)
    daydata = daydata.loc[(daydata['route'].values.astype(np.int) == args.route) &
                          (daydata['time'] >= args.hourstart*3600) &
                          (daydata['time'] <= args.hourend*3600) ]
    daydata = binData(daydata)

    print('Day columns = ', daydata.columns)

    print('Reading baseline data')
    baselinedata = pd.read_csv(args.baseline)
    print('Baseline columns = ', baselinedata.columns)

    print('Merging')
    merged = pd.merge(daydata, baselinedata, how='inner', on=['binlat','binlon','bintime','binheading'])
    merged['speeddiffz'] = (merged['speed']-merged['mean'])/(merged['std'])

    print('Writing')
    merged.to_csv(args.output)

