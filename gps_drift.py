
""" Drift correction with additional GPS trackers.
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


def modify_tracks(track_1, track_2):
    """ Function for track correction.
        The distance between GPS trackers does not change during the measurement time.
        Therefore both tracks can be smoothened decreasing the coordinate error.
    """
    pass


def filter_outliers(track):
    pass


def __detect_time(x):
    return pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')


def __new_point(t):
    pass


if __name__ == '__main__':
    pass
    inp_fld = '/home/dm/work/data/tryoshnikov/EM/04-26/gps/'
    inp_file_1 = 'gps_1_orange.csv'
    inp_file_2 = 'gps_2_blue.csv'
    inp_file_3 = 'gps_3_yellow.csv'
#    gps_track = pd.read_csv(inp_fld + inp_file_1)
#    drift = estimate_drift(gps_track)
#    print(drift.head())
    track = interpolate_tracks([inp_fld + inp_file_1, inp_fld + inp_file_2])
    print(track.columns)
    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(track[(1, 'lon')], track[(1, 'lat')], color='orange')
    plt.plot(track[(2, 'lon')], track[(2, 'lat')], color='blue')
    plt.plot((track[(1, 'lon')] + track[(2, 'lon')]) / 2., (track[(1, 'lat')] + track[(2, 'lat')]) / 2., color='green')
    plt.show()

    '''
    start_time = max(track_1.time[0], track_2.time[0])
    end_time = min(track_1.time[track_1.shape[0] - 1], track_2.time[track_2.shape[0] - 1])
    track_1 = track_1.between_time(start_time.time(), end_time.time())
    track_2 = track_2.between_time(start_time.time(), end_time.time())
    extention_2 = [__new_point(t, track_2) for t in track_1.time if t not in track_2.time]
    for t in track_1.time:
        if t in track_2.time:
            continue
        extention_2.append([t, 90, 360])
    '''
