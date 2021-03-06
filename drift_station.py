""" Some tools for observations on a floating ice.
"""
import pandas as pd


class IceFloe(object):
    """ Basic class for an ice floe.
    """
    def __init__(self, name, heading, desc=''):
        self.name = name
        self.desc = desc
        self.heading = heading
        """ Zero point is a pandas dataframe with gps coordinates of the (0, 0) point on the ice floe. """
        self.zero_point = pd.DataFrame()
        """ Unit point is a pandas DataFrame with GPS coordinates of the (unit, 0) point on the ice flow.
            This is the point that defines the direction of the x (or y) axis.
        """
        self.unit_point = pd.DataFrame()
    
    def calculate_drift(self, timepoint_1, timepoint_2):
        return True

    def visualise_rotation(self, timepoint_1, timepoint_2):
        return True
    
    def global2local(self, lat, lon, time):
        return True
    
    def local2global(self, x, y, time=''):
        return True
    
    def extend_reference_point_serie(self, point_id, data):
        """ Extend the time and coordinates (lat, lon) of the zero point.
            Data is expected to be a pandas DataFrame with the following columns:
            lat, lon, time (UTC)
            point_id can be either 'zero' or 'unit'
        """
        if 'lat' not in data.columns or 'lon' not in data.columns or 'time' not in data.columns:
            print('Input data is expected to contain the following columns: "lat", "lon", "time".')
            print('The input data has the following columns: {0}'.format(data.columns))
            return False
        if data.shape[1] >= 3:
            data_new = data.filter(items=['lat', 'lon', 'time'])
        else:
            data_new = data
        if point_id.lower() == 'zero':
            self.zero_point = pd.concat([self.zero_point, data_new], ignore_index=True)
        elif point_id.lower() == 'unit':
            self.unit_point = pd.concat([self.unit_point, data_new], ignore_index=True)
        else:
            print('Wrong point_id. Possible values are "zero", "unit". Given value is {0}'.format(point_id))
            return False
        return True
    

if __name__ == '__main__':
    pass
