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

from read_gpx import read_gpx


def estimate_drift(gps_data):
    """ Input is expected to be a pandas dataframe with lat, lon, and time columns
    """
    d_lat = gps_data['lat'].diff()
    d_lon = gps_data['lon'].diff()
    drift = pd.DataFrame()
    drift['d_lat'] = d_lat
    drift['d_lon'] = d_lon
    return drift


if __name__ == '__main__':
    inp_file_1 = ''
    inp_file_2 = ''
    inp_file = '/home/dm/work/data/tryoshnikov/EM/gps1/Track_2019-03-30 102146.gpx'
    gps_track = read_gpx(inp_file)
    drift = estimate_drift(gps_track)
    print(drift.head())

