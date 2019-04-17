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


def estimate_drift():
    pass


if __name__ == '__main__':
    inp_file_1 = ''
    inp_file_2 = ''
