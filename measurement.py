""" PointMeasurement class definition.
"""

class PointMeasurement(object):
    def __init__(self, data, coordinates, timestamp):
        self.data = data
        self.coordinates = coordinates
        self.timestamp = timestamp

    def location_at_time(self, timestamp):
        """ Calculate GPS coordinates of the measurement at the given time.
        """
        pass
