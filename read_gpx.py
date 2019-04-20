""" Read .gpx files produced by GPS devices (like Garmin GPSMAP64s)
    and convert into a .csv file.
"""

import pandas as pd
import datetime
from xml.etree import ElementTree


def read_gpx(inp_file, time_format='%Y-%m-%dT%H:%M:%SZ'):
    gpx = ElementTree.parse(inp_file).getroot()
    coords = [{'lat': float(point.get('lat')),
               'lon': float(point.get('lon')),
               'time': datetime.datetime.strptime(point[1].text, time_format),
               'elevation': float(point[0].text)} for point in gpx[1][4]]
    data = pd.DataFrame(coords)
    return data



if __name__ == '__main__':
    inp_file = '/home/dm/work/data/tryoshnikov/EM/gps1/Track_2019-03-30 102146.gpx'
    out_file = '/home/dm/gps_test.csv'
    data = read_gpx(inp_file)
    data.to_csv(out_file)
