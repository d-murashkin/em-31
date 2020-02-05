""" Layer class definitino """

class Layer(object):
    def __init__(self, data, resolution, projection, timestamp, desc=''):
        self.desc = desc
        self.projection = projection
        self.data = data
        self.timestamp = timestamp
        self.resolution = resolution
