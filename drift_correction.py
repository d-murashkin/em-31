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
import pandas as pd
import numpy as np

from read_gpx import read_gpx


def estimate_drift(gps_data):
    """ Input is expected to be a pandas dataframe with lat, lon, and time columns
    """
    R = 6400000             # Earth radius
    base_point_index = 0
    base_lat = gps_data['lat'][base_point_index]
    base_lon = gps_data['lon'][base_point_index]
    base_time = gps_data['time'][base_point_index]
    lat_rel = gps_data['lat'] - base_lat
    lon_rel = gps_data['lon'] - base_lon

    d_lat = gps_data['lat'].diff()
    d_lon = gps_data['lon'].diff()
    d_angle = np.arccos(np.sin(gps_data['lon']) * np.sin(gps_data['lon'].shift(1)) + np.cos(gps_data['lon']) * np.cos(gps_data['lon'].shift(1)) * np.cos(gps_data['lat'].diff()))
    d_lat_meters = d_lat / 180. * np.pi * R
    d_lon_meters = d_lon / 180. * np.pi * R * np.cos(gps_data['lat'])
#    d_abs_meters = np.linalg.norm(d_lat_meters, d_lon_meters)
    d_abs_meters = (d_lat_meters**2 + d_lon_meters**2)**0.5
    d_time = gps_data['time'].diff()
    d_time_sec = pd.Series([i.seconds for i in d_time])
    d_rate = d_abs_meters / d_time_sec

    drift = pd.DataFrame()
    drift['d_lat'] = d_lat
    drift['d_lon'] = d_lon
    drift['drift_meters'] = d_abs_meters
    drift['drift_rate'] = d_rate
    drift['d_time_sec'] = d_time_sec
    drift['d_angle'] = d_angle
    drift['time'] = gps_data['time']
    return drift


def correct_uniform_drift(df, start_index, end_index):
    """ Uniform drift correction (without any additional GPS data available).
        Start and end point must be located at the same place of the ice floe.
    """
    lat_start = df.lat[start_index]
    lon_start = df.lon[start_index]
    lat_end = df.lat[end_index]
    lon_end = df.lon[end_index]
    dt = df.timestamp - df.timestamp[start_index]
    d_lat = (lat_end - lat_start) / (df.timestamp[end_index] - df.timestamp[start_index])
    d_lon = (lon_end - lon_start) / (df.timestamp[end_index] - df.timestamp[start_index])
    df['lat_corr'] = df.lat - d_lat * dt
    df['lon_corr'] = df.lon - d_lon * dt
    return True


if __name__ == '__main__':
    pass
    '''
    inp_file_1 = ''
    inp_file_2 = ''
    inp_file = '/home/dm/work/data/tryoshnikov/EM/gps1/Track_2019-03-30 102146.gpx'
    gps_track = read_gpx(inp_file)
    drift = estimate_drift(gps_track)
    print(drift.head())
#    from matplotlib import pyplot as plt
#    plt.figure()
#    plt.scatter(drift['d_lat'], drift['d_lon'])
#    plt.show()
    '''
    inp_file = '/home/dm/work/data/tryoshnikov/EM/22apr/prepr/042213A.csv'
    data = pd.read_csv(inp_file)
    correct_uniform_drift(data, 0, len(data) - 1)
    from matplotlib import pyplot as plt
    plt.scatter(data.lat_corr, data.lon_corr)
    plt.scatter(data.lat, data.lon)
    plt.show()
