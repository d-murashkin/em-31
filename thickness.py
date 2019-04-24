""" Estimate sea ice and snow thickness from EM-31 measurements
"""
import numpy as np
import pandas as pd


if __name__ == '__main__':
    calibration_heights = np.array([12, 32, 45, 55, 62, 70, 86, 95, 110, 120, 145, 168, 191, 212, 225])
    calibration_values = np.array([905, 808, 738, 690, 646, 608, 540, 491, 437, 389, 340, 289, 239, 210, 182])
    calibration_true_ice_thicknesses = np.array([72, 70, 71, 70, 72, 71])
    if calibration_heights.shape != calibration_values.shape:
        print('Number of calibration heights does not correcpond to the number of calibration measurements.')
    fit_func = np.polyfit(np.log(calibration_values), calibration_heights + calibration_true_ice_thicknesses.mean(), 1)
    print(fit_func)

    inp_file = '~/work/data/tryoshnikov/EM/22apr/prepr/042213A.csv'
    height = 35         # Height of the EM above the snow surface
    em_values = pd.read_csv(inp_file)['data']
    print(fit_func)
    distance = fit_func[1] + fit_func[0] * np.log(em_values)
    ice_and_snow = distance - height
