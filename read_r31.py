""" Script for reading EM-31 log files (*.R31) and convertion into a csv file
"""

import datetime as dtm
import argparse
import sys

import pandas as pd


def read_r31(inp_filename, date=''):
    if date:
        timeformat = '%Y%m%d%H%M%S.00'
    else:
        timeformat = '%H%M%S.00'

    with open(inp_filename, 'r') as f:
        d = f.readlines()

    preprocessed_data = []
    lat = None
    lon = None
    timestamp = None
    for i, line in enumerate(d):
        if '@$GPGGA' in line:
            time = dtm.datetime.strptime(date + line.split(',')[1], timeformat)
            timestamp = dtm.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).seconds
            lat1 = line.split(',')[-1]
            lat2 = d[i + 1].split(',')[0]
            lat_str = lat1[:-1] + lat2[1:]
            try:
                lat = float(lat_str) / 100.
            except:
                continue
                pass
            try:
                lon = d[i + 1].split(',')[2]
            except:
                pass
            lon = float(lon) / 100.
            
        if 'data:' in line and lat and lon:
            datavalue = line.split('-')[1]
            if '+' in datavalue:
                datavalue = datavalue.split('+')[0]
    
            preprocessed_data.append({'lat': lat,
                                      'lon': lon,
                                      'data': int(datavalue) / 4.,
                                      'timestamp': timestamp,
                                      'time': time,
                                      })
    
    q = pd.DataFrame(preprocessed_data)
    return q


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert *.R31 file from EM-31 into a csv. Input and output files should be provided with -i and -o options.')
    parser.add_argument('-i', help='input filename')
    parser.add_argument('-o', help='output filename')
    parser.add_argument('-d', help='date in the format %Y%m%d.')
    args = parser.parse_args()
    if not args.o:
        print('Please, specify output file with -o option.')
        sys.exit()
    if not args.i:
        print('Please, specify input file with -i option.')
        sys.exit()
    
    if args.d:
        data = read_r31(args.i, args.d)
    else:
        data = read_r31(args.i)

    data.to_csv(args.o)
