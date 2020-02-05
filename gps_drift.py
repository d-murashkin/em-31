
""" Drift correction with additional GPS trackers.
    Since distance between GPS trackers does not change, it can be used to improve position error (to be implemented).
    Two or more tracks gives opportunity to filter out outlying point of GPS track (to be implemented).
"""
import numpy as np
import pandas as pd


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


def interpolate_tracks(track_file_list, frequency='1S'):
    """ Function creates a pandas DataFrame with both trackes interpolated for given frequency.
        Default frequency is one second.
        This means that there are GPS two coordinates for each second.
    """
    """ Read and join GPS tracks. """
    tracks = [read_track(item) for item in track_file_list]
    joined_tracks = pd.concat(tracks, axis='columns', join='outer', keys=np.arange(1, len(tracks) + 1))

    """ Create a new pandas DataFrame. """
    start_time = min([item.time[0] for item in tracks])
    end_time = max([item.time[item.shape[0] - 1] for item in tracks])
    track = pd.DataFrame(pd.date_range(start=start_time, end=end_time, freq=frequency))
    track.columns = ['time']

    """ Interpolate all GPS tracks. """
    track = track.join(joined_tracks, on='time', how='outer')
    track = track.drop(columns=[(i + 1, 'time') for i, _ in enumerate(tracks)])
    for i, _ in enumerate(tracks):
        track[(i + 1, 'lat')].interpolate(method='linear', inplace=True)
        track[(i + 1, 'lon')].interpolate(method='linear', inplace=True)
    track.index = track.time
    track.dropna(axis='index', how='any', inplace=True)
    return track


def read_track(track_file):
    """ Read GPS track """
    track = pd.read_csv(track_file)
    track['time'] = track.time.apply(__detect_time)
    track.index = track.time
    track = track.filter(['lat', 'lon', 'time'])
    return track


def __detect_time(x):
    return pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')


def calculate_drift(tracks, zero_time):
    """ Calculate drift for every timepoint from tracks.
        The drift is calculated relativly to the zero_time (time of zero drift).
        *tracks* is expected to be a pandas dataframe.
        *zero_time* should be datetime.datetime / pandas.datetime or similar data type.
    """
    """ Check input data type """
    if type(tracks) is not pd.DataFrame:
        print("Input data is expected to be a pandas DataFrame.")
        return False
    if type(zero_time) is not pd.datetime:
        print("zero_time is expected to be a datetime.datetime or pandas.datetime type.")
        return False


if __name__ == '__main__':
    pass
    inp_fld = '/home/dm/work/data/tryoshnikov/EM/04-26/gps/'
    inp_file_1 = 'gps_1_orange.csv'
    inp_file_2 = 'gps_2_blue.csv'
    inp_file_3 = 'gps_3_yellow.csv'
    track = interpolate_tracks([inp_fld + inp_file_1, inp_fld + inp_file_2])
    print(track.columns)

    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(track[(1, 'lon')], track[(1, 'lat')], color='orange')
    plt.plot(track[(2, 'lon')], track[(2, 'lat')], color='blue')
    plt.plot((track[(1, 'lon')] + track[(2, 'lon')]) / 2., (track[(1, 'lat')] + track[(2, 'lat')]) / 2., color='green')
    plt.show()
