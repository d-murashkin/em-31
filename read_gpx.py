""" Read .gpx files produced by GPS devices (like Garmin GPSMAP64s)
    and convert into a .csv file.
"""
import argparse
import sys

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
    parser = argparse.ArgumentParser(description='Convert *.gpx files created by GPS navigators into *.csv files. Input and output files should be specified with -i and -o options.')
    parser.add_argument('-i', help='input filename')
    parser.add_argument('-o', help='output filename')
    args = parser.parse_args()

    """ Check mandatory arguments """
    if not args.i:
        print('Please, specify input file with -i option.')
        sys.exit()
    if not args.o:
        print('Please, specify output file with -o option.')

    data = read_gpx(args.i)
    data.to_csv(args.o)
