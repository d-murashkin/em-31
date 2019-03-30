""" Read .gpx files produced by GPS devices (like Garmin GPSMAP64s)
    and convert into a .csv file.
"""

import pandas as pd
from xml.etree import ElementTree


if __name__ == '__main__':
    inp_file = '/media/dmitrii/GARMIN/Garmin/GPX/Track_2019-03-30 102146.gpx'
    out_file = '/home/dmitrii/gps_test.csv'
    gpx = ElementTree.parse(inp_file).getroot()
    coords = []
    for point in gpx[1][4]:
        coord = {'lat':float(point.get('lat')), 'lon':float(point.get('lon')), 'time':point[1].text, 'elevation':float(point[0].text)}
        coords.append(coord)
    data = pd.DataFrame(coords)
    data.to_csv(out_file)
