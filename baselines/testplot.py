import gmplot
import argparse
import pandas as pd
import numpy as np

if __name__=="__main__":
    gmap = gmplot.GoogleMapPlotter(43.7000, -79.4, 11)

    baseline = pd.read_csv('last-2week-september.csv')
#    event    = pd.read_csv('longer.csv')

    gmap.scatter(baseline['binlat'], baseline['binlon'], '#3B0B39', size=40, marker=False)
#    gmap.heatmap(event['lat'], event['lon'])

    gmap.draw("mymap.html")
