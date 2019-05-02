
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

if __name__ == '__main__':

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