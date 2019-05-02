""" Script for drift correction.
    There are 3 ways to correct the drift.
    The first one is to be used when no additional to EM GPS data is available.
    In this case the first and the last point of measurements should be the same.
    The drift is assumed to be continious with the constant rate.
    The rotation is neglected.
    The second option should be used when only one additional GPS tracked was used
    during the EM survey.
    In this case drift is calculated with the assumption that rotation of the ice flow
    can be neglected.
    The third way to accuout for the drift is to use two GPS trackers located at a
    distance of ~50 meters or more.
    In this case both components of the drift are calculated: movement and rotation.
"""
import argparse
import sys

import pandas as pd


def correct_uniform_drift(df, start_index=0, end_index=None):
    """ Uniform drift correction (without any additional GPS data available).
        Start and end point must be located at the same place of the ice floe.
        Input pandas DataFrame is expected to have the following columns:
        'lat', 'lon', 'timestamp', 'time'.
        This function modifies the dataframe by adding the following columns:
        'lat_corr', 'lon_corr', 'time_corr' with corrected values for latitude, longitude, and
        time when those corrected values are valid (corrected values are calculated as they were at the time_corr).
    """
    if type(df) is not pd.DataFrame:
        print('Input is expected to be a pandas DataFrame, not {0}'.format(type(df)))
        return False

    if end_index is None:
        end_index = df.shape[0] - 1
    
    if end_index <= start_index:
        print('End point index is expected to be larger than the start index.')
        return False
    
    if 'lat' not in df.columns:
        print('Input pandas DataFrame does not have "lat" column.')
        return False
    if 'lon' not in df.columns:
        print('Input pandas DataFrame does not have "lon" column.')
        return False
    if 'time' not in df.columns:
        print('Input pandas DataFrame does not have "time" column.')
        return False
    if 'timestamp' not in df.columns:
        print('Input pandas DataFrame does not have "timestamp" column.')
        return False

    lat_start = df.lat[start_index]
    lon_start = df.lon[start_index]
    lat_end = df.lat[end_index]
    lon_end = df.lon[end_index]
    dt = df.timestamp - df.timestamp[start_index]

    d_lat = (lat_end - lat_start) / (df.timestamp[end_index] - df.timestamp[start_index])
    d_lon = (lon_end - lon_start) / (df.timestamp[end_index] - df.timestamp[start_index])

    df['lat_corr'] = df.lat - d_lat * dt
    df['lon_corr'] = df.lon - d_lon * dt
    df['time_corr'] = df['time'][start_index]
    return True


if __name__ == '__main__':
    desc = """Apply uniform drift correction.
              Choose two points of the track, where location on an ice floe is the same.
              Based on these points the drift rate is estimated assuming its uniform.
              Arguments:
                -i input    data file
                -o output   data file (optional)
                -savefig    path to the figure with the result (optional)
                -showfig    if specified the figure with the result is shown
                -start      id of the starting point, default is 0
                -end        id of the end point, default is the last point of the track
           """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', help='input data file')
    parser.add_argument('-o', help='output data file')
    parser.add_argument('-savefig', help='save figure of the result')
    parser.add_argument('-showfig', help='show figure of the result')
    parser.add_argument('-start', help='id of the starting point, default is 0')
    parser.add_argument('-end', help='id of the end point, default is the last point in the data')
    args = parser.parse_args()

    """ Check mandatory arguments """
    if not args.i:
        print('Specify input file with -i option.')
        sys.exit()
    
    """ Set optional arguments """
    if not args.start:
        args.start = 0
    if not args.end:
        args.end = None

    try:
        data = pd.read_csv(args.i)
    except:
        print('Input is expected to be a *.csv file. Could not read the input file.')
        sys.exit()
    ret = correct_uniform_drift(data, start_index=args.start, end_index=args.end)
    if not ret:
        print('Something went wrong during the correction. Check messages above.')
        sys.exit()

    if not args.o:
        print('Output file is not specified, results are not saved.')
        print('To save result specify output file with -o option')
    else:
        data.to_csv(args.o)
    if not args.showfig and not args.savefig:
        sys.exit()

    from matplotlib import pyplot as plt
    plt.scatter(data.lon, data.lat)
    plt.scatter(data.lon_corr, data.lat_corr)
    plt.title('Results of the drift correction.')
    plt.xlabel('Longitude, deg')
    plt.ylabel('Latitude, deg')
    plt.legend(['Measured track', 'Corrected track'])
    plt.colorbar()
    if args.savefig:
        plt.savefig(args.savefig)
    if args.showfig:
        plt.show()
