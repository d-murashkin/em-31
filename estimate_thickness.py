""" Estimate sea ice and snow thickness from EM-31 measurements
"""
import argparse
import sys

import numpy as np
import pandas as pd


def estimate_height(df, calibration_csv, em_height):
    """ Function estimates hight of the EM device above the water-ice interface.
        Exponential fit for calibration data is used.
        *calibration* is expected to be a *.csv file with the following coluns:
        'height' and 'value' for calibration points, and 'ice_thickness' with some contact measurements of sea ice thickness.
        *em_height* is the height if the EM device above the snow surface.
        This function modifies the input DataFrame by adding the following column(s):
        'ice_and_snow'.
    """
    if type(df) is not pd.DataFrame:
        print('df is expected to be a pandas DataFrame structure with "data" column.')
        return False

    if 'data' not in df.columns:
        print('Input DataFrame does not have "data" column.')
        return False

    try:
        calibration = pd.read_csv(calibration_csv)
    except:
        print('Could not read the calibration csv file {0}.'.format(calibration_csv))
        return False
    """ Check for the required columns in the calibration data. """
    if 'height' not in calibration.columns:
        print("The 'height' column is not found in the calibration csv file.")
        return False
    if 'value' not in calibration.columns:
        print("The 'value' column is not found in the calibration csv file.")
        return False
    if 'ice_thickness' not in calibration.columns:
        print("The 'ice_thicknes' column is not found in the calibration csv file.")
        return False
    
    average_ice_thickness = calibration.ice_thickness.mean()
    fit_function = np.polyfit(np.log(calibration.value), calibration.height + average_ice_thickness, 1)
    df['ice_and_snow'] = fit_function[1] + fit_function[0] * np.log(df.data) - em_height
    return True


if __name__ == '__main__':
    desc = """ Script calculates sum of snow and ice thickness for data collected with EM device.
               Exponential fit for calibration data is used.
               Arguments:
               -i           input file
               -o           output file
               -cal         calibration csv file
               -em_height   height of the EM device above the snow surface
            All the arguments above should be specified.
           """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', help='Input file name.')
    parser.add_argument('-o', help='Output file name.')
    parser.add_argument('-cal', help='Calibration csv file.')
    parser.add_argument('-em_height', help='EM device height above the snow surface.')
    args = parser.parse_args()

    """ Check mandatory arguments """
    if not args.i:
        print('Input file name should be specified with -i option.')
        sys.exit()
    if not args.cal:
        print('Calibration csv file should be specified with -cal option.')
        sys.exit()
    if not args.em_height:
        print('EM device hight above the snow surface should be specified with -em_height option.')
        sys.exit()
    if not args.o:
        print('Output file name should be specified with -o option.')
        sys.exit()
    
    try:
        data = pd.read_csv(args.i)
    except:
        print('Unable to read csv file {0}'.format(args.i))
        sys.exit()
    res = estimate_height(data, args.cal, args.em_height)
    if not res:
        print('Something went wrong during the ice and snow thicknes calculation. Check messages above.')
        sys.exit()
    
    data.to_csv(args.o)

    """
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
#    inp_fld = '/home/dm/work/data/tryoshnikov/EM/13apr/prepr/'
#    out_fld = '/home/dm/work/data/tryoshnikov/EM/13apr/results/'
    inp_fld = '/home/dm/work/data/tryoshnikov/EM/01may/prepr/'
    out_fld = '/home/dm/work/data/tryoshnikov/EM/01may/results/'
#    items = ['041309A.csv', '041310A2.csv', '041310A3.csv', '041310A5.csv', '041311A6.csv']
    items = ['050110A.csv', '050111A2.csv']
    out_file = out_fld + ''.join([i[:-4] for i in items]) + '.csv'

    height = 35         # Height of the EM above the snow surface
#    height = 46
    data = pd.concat([pd.read_csv(inp_fld + item) for item in items], axis=0, ignore_index=True)
    print(data.shape)
    correct_uniform_drift(data, 0, len(data) - 1)
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
    """
