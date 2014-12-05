#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# dealing with filenames
import os.path
# for formatting timestamps
import time
# using izip rather than zip
import itertools
# downloading data
import urllib2
# uncompress data
import gzip
# unmarshalling JSON data
import json
# for showing a sample
import copy
import pprint

from argparse import ArgumentParser

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plot

#date_format="%Y-%m-%d:%H-%M"
date_format="%Y-%m-%d"

KELVIN=273.15

def xpath (entry, path):
    """
    helper function to extract a piece from a complex data 
    using a succession of keys or indices
    e.g.
    if dict = {'city': {'coord': {'lat': 49.55, 'lon': 1.62}}}
    then
    xpath (dict, ('city', 'coord', 'lon')) returns 1.62
    and
    xpath (dict, 'city/coord/lon')) returns 1.62 as well
    """
    if isinstance (path, str):
        path = path.split('/')
    result=entry
    for key in path: result=result[key]
    return result


# like in css we do: top right bottom left
class RectangleArea(object):
    def __init__(self, *args):
        """
        constructor
        can take either 4 numbers top, right, bottom and left
        or a single string with these values comma-separated
        
        known limitation : cannot select a rectangle
        over the international date line
        """
        # 4 arguments - we need numbers then
        if len(args) == 4:
            self.corners = tuple(args)
        # 1 argument - a string then
        elif len(args) == 1:
            self.corners = [ float(x) for x in args[0].split(',') ]

    def __repr__(self):
        return "Top {} Right {} Bottom {} Left {}".format(*self.corners)

    def covers_lat_lon(self, lat_lon_rec):
        """
        tells if a point, represented as a dict with the
        'lat' and 'lon' keys as in the native JSON format,
        belongs in this area
        
        return a bool
        """
        (top, right, bottom, left) = self.corners
        lon = lat_lon_rec['lon']
        lat = lat_lon_rec['lat']
        return lon >= left and lon <= right and\
               lat >= bottom and lat <= top

    def covers_city(self, city):
        return self.covers_lat_lon(xpath (city, 'city/coord'))

def load_cities (filename):
    """
    This function loads a JSON file
    which may be gzipped

    returns a list of city-records
    or None if if was not possible to open that file
    """
    if not os.path.isfile(filename):
        return None
    # try to decode a plain file
    try:
        with open(filename) as input:
            return [ json.loads(line) for line in input if line ]
    except:
        pass
    # try to decode a gzipped file
    try:
        with gzip.open(filename) as input:
            return [ json.loads(line) for line in input if line ]
    except:
        pass
    return None
    
# used to produce the text for the notebook
def show_sample_city (city_record):
    """
    used to produce the notebook that describes the exercise

    pretty print a city record 
    with only the first data record mentioned
    """
    sample = copy.deepcopy(city_record)
    data = xpath(sample, 'data' )
    data[1:] = [ '... other similar dicts ...']
    pprint.pprint (sample)

def plot_2d (cities):
    """
    visualize the positions of all cities on a 2D map
    """
    LON_s = [ xpath(city, 'city/coord/lon') for city in cities ]
    LAT_s = [ xpath(city, 'city/coord/lat') for city in cities ]
    # emphasize selected cities with a specific size and color
    # 'r' stands for red, 'b' is black
    colors = [ 'r' if  'selected' in city else 'b' for city in cities ]
    sizes = [ 30 if 'selected' in city else 1 for city in cities ]
    plot.scatter(LON_s, LAT_s, c=colors, s=sizes)

    # to exit the drawing, close related window
    plot.show()


def plot_3d (cities):
    """
    visualize in 3D 
    position as (x, y) and temperature as z
    
    to keep it simple we take the temperature from
    . the first measure available in each city
    . the 'day' field in the 'temp' section, that is
      to say the average that day
    . also we translate into Celsius degrees

    likewise date is extracted from the first city 
    as a rough approximation
    """

    # base all measures on first day present in each city
    day = 0
    # date time for the label
    dt = xpath(cities[0], ('data',day,'dt'))
    date=time.strftime(date_format,time.gmtime(dt))
    
    fig = plot.figure()
    ax = fig.gca(projection='3d')
    X = [ xpath (city, ('city','coord','lon')) for city in cities ]
    Y = [ xpath (city, ('city','coord','lat')) for city in cities ]
    T_celsius = [ xpath (city, ('data',day,'temp','day')) - KELVIN for city in cities ]
    ax.plot_trisurf(X,Y,T_celsius, cmap=cm.jet, linewidth=0.2,
                    label="Average temperature on %s"%date)
    ax.set_title ("Temperature on %s"%date)
    plot.show()

    
def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--crop", dest='crop', default=None,
                        help="""specify a region for cropping
                        regions are rectangular areas and can be specified 
                        as a comma-separated list of 4 numbers for
                        north, east, south, west""")
    parser.add_argument("-n", "--name", dest='names', default=[],
                        action='append',
                        help="cumulative - select cities by this name(s)")
    parser.add_argument("-l", "--list", dest="list_cities", default=False,
                        action='store_true',
                        help="If set, selected city names get listed")
    parser.add_argument("-2", "--2d", dest="plot_2d", default=False,
                        action='store_true',
                        help="""Display a 2D diagram of the 
                        positions of selected cities""")
    parser.add_argument("-3", "--3d", dest="plot_3d", default=False,
                        action='store_true',
                        help="""Display a 3D diagram of the 
                        pressure of selected cities""")

    parser.add_argument("filename",help="input JSON file - might be gzipped")
    args = parser.parse_args()

    # always load input file
    cities = load_cities(args.filename)
    if not cities:
        print ("Cannot open input {}".format(args.filename))
        return 1
    print (10*'-', "From {}\n\tdealing with {} cities".\
           format(args.filename, len(cities)))

    # crop if specified
    if args.crop:
        crop_area = RectangleArea(args.crop)
        cities = [city for city in cities if crop_area.covers_city(city)]
        print (10*'-', "After cropping with {}\n\tdealing with {} cities".\
               format(crop_area, len(cities)))

    # mark the ones selected by their name if specified with --name
    if args.names:
        # lowercase all
        args.names = [ name.lower() for name in args.names ]
        selected = 0
        for city in cities:
            if xpath(city, 'city/name').lower() in args.names:
                city['selected'] = True
                selected += 1
        print (10*'-', "Selected {} cities with name(s)\n\t{}".\
               format(selected, args.names))

    # display selected cities by name and # of measures with --list
    if args.list_cities:
        cities.sort(key=lambda city: xpath(city, 'city/name'))
        for city in cities:
            print ("{} ({} measures)".format(xpath(city, 'city/name'),
                                            len(xpath(city, 'data'))))

    # show plots as requested
    if args.plot_2d:
        plot_2d(cities)

    # show plots as requested
    if args.plot_3d:
        plot_3d(cities)


if __name__ == '__main__':
    main()
