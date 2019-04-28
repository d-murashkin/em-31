""" Estimate sea ice and snow thickness from EM-31 measurements
"""
import os

import numpy as np
import pandas as pd

from drift_correction import correct_uniform_drift


if __name__ == '__main__':
    calibration_heights = np.array([12, 32, 45, 55, 62, 70, 86, 95, 110, 120, 145, 168, 191, 212, 225])
    calibration_values = np.array([905, 808, 738, 690, 646, 608, 540, 491, 437, 389, 340, 289, 239, 210, 182])
    calibration_true_ice_thicknesses = np.array([72, 70, 71, 70, 72, 71])
    if calibration_heights.shape != calibration_values.shape:
        print('Number of calibration heights does not correcpond to the number of calibration measurements.')
    fit_func = np.polyfit(np.log(calibration_values), calibration_heights + calibration_true_ice_thicknesses.mean(), 1)

#    inp_file = '~/work/data/tryoshnikov/EM/22apr/prepr/042213A.csv'
#    out_file = '~/work/data/tryoshnikov/EM/22apr/results/042213A.csv'
##    inp_fld = '~/work/data/tryoshnikov/EM/12apr/prepr/'
##    out_fld = '~/work/data/tryoshnikov/EM/12apr/results/'
##    items = ['041211Am.csv', '041212A2.csv', '041212A3.csv']
###    inp_fld = '/home/dm/work/data/tryoshnikov/EM/14apr/prepr/'
###    out_fld = '/home/dm/work/data/tryoshnikov/EM/14apr/results/'
###    items = ['041413Al.csv', '041414A2.csv', '041414A3.csv', '041415A4.csv']
    inp_fld = '/home/dm/work/data/tryoshnikov/EM/13apr/prepr/'
    out_fld = '/home/dm/work/data/tryoshnikov/EM/13apr/results/'
    items = ['041309A.csv', '041310A2.csv', '041310A3.csv', '041310A5.csv', '041311A6.csv']
    out_file = out_fld + ''.join([i[:-4] for i in items]) + '.csv'

    height = 35         # Height of the EM above the snow surface
#    height = 46
    data = pd.concat([pd.read_csv(inp_fld + item) for item in items], axis=0, ignore_index=True)
    print(data.shape)
#    correct_uniform_drift(data, 0, len(data) - 1)
    correct_uniform_drift(data, 2600, 3700)
    em_values = data['data']
    distance = fit_func[1] + fit_func[0] * np.log(em_values)
    ice_and_snow = distance - height
    data['ice_and_snow'] = ice_and_snow
    data.to_csv(out_file)

    print(data.columns)

    from matplotlib import pyplot as plt
    plt.scatter(data.lat_corr, data.lon_corr)
#    plt.scatter(data.lat, data.lon, c=data['Unnamed: 0'])
    plt.scatter(data.lat, data.lon)
#    plt.colorbar()
    plt.show()
