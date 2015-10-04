#!/usr/bin/bash

import pandas as pd
import numpy as np
import sys
import time
import datetime as dt
import matplotlib.pyplot as plt

data = pd.read_csv('last-2week-september.csv').dropna()


reliability = np.divide(data['std'].values,data['mean'].values)
means = data[data['mean'] > 0.1]['mean']*3.6
stds = data['std']*3.6


plt.figure()
binwidth = 0.1
plt.title(r'Unreliability$=\sigma/\mu$ August and September Weekdays')
plt.hist(reliability,bins=np.arange(min(reliability), max(reliability) + binwidth, binwidth), color='r')
plt.ylabel('Count')
plt.savefig('reliability.png')


plt.figure()
binwidth = 1
plt.hist(np.asarray(means), bins=np.arange(min(means), max(means) + binwidth, binwidth),color='g')
plt.xlabel('kph')
plt.ylabel('Count')
plt.savefig('speeds.png')

plt.figure()
binwidth = 1
plt.hist(np.asarray(stds), bins=np.arange(min(stds), max(stds) + binwidth, binwidth), color='b')
plt.xlabel('kph')
plt.ylabel('Count')
plt.savefig('stds.png')