#!/usr/bin/env python

from __future__ import print_function
import pandas as pd
import numpy as np
import pyproj
import time
import argparse
import os

def groupData(data, minpts=5):
    grouped = data.groupby(['binlat','binlon','bintime','binheading'])
    grouped = pd.DataFrame(grouped['speed'].agg([len, np.mean, np.std]))
    grouped = grouped.loc[grouped.len > 5]
    return grouped

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs="+", help="Raw input csv files")
    parser.add_argument('-v','--maxspeed', type=float, default=15.)
    parser.add_argument('-o','--output', type=str, default="grouped.csv", help="Output file name")
    args = parser.parse_args()

    proj = pyproj.Proj("+proj=utm +zone=17N, +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    allbinned = []
    for filename in args.infile:
        data = pd.read_csv(filename)
        grouped = data.groupby(['binlat','binlon','binheading'])['bintime'].agg(np.max)

        basename = os.path.splitext(filename)[0]
        grouped.to_csv(basename+"-max-over-time.csv")
