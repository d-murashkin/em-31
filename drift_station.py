""" Some tools for observations on a floating ice.
"""

class IceFloe(object):
    """ Basic class for an ice floe.
    """
    def __init__(self, name, heading, desc=''):
        self.name = name
        self.desc = desc
        self.heading = heading
    
    def calculate_drift(self, timepoint_1, timepoint_2):
        return True

    def visualise_rotation(self, timepoint_1, timepoint_2):
        return True


if __name__ == '__main__':
    pass