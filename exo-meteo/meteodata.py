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

date_format="%Y-%m-%d:%H-%M"

def xpath (entry, path):
    """
    helper function to extract a piece from a complex data 
    using a succession of keys or indices
    e.g.
    if dict = {'city': {'coord': {'lat': 49.55, 'lon': 1.62}}}
    then
    xpath (dict, ('city', 'coord', 'lon')) returns 1.62
    """
    result=entry
    for key in path: result=result[key]
    return result


# like in css we do: top right bottom left
class RectangleArea(object):
    def __init__(self, top, right, bottom, left):
        """
        constructor
        """
        self.corners = (top, right, bottom, left)

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
        return self.covers_lat_lon(xpath (city, ('city', 'coord')))

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
    
def show_sample_city (city_record):
    """
    pretty print a city record
    """
    sample = copy.deepcopy(city_record)
    data = xpath(sample, ('data',) )
    data[1:] = [ '... other similar dicts ...']
    print ("Sample city")
    pprint.pprint (sample)

def foo():

    print (40*'=')
    url = "http://78.46.48.103/sample/daily_14.json.gz"

    print ("Téléchargement de %s ..."%url)
    network_file=urllib2.urlopen(url)
    compressed_json=network_file.read()
    print ("OK - %s téléchargés"%megas(len(compressed_json)))
    uncompressed_json=zlib.decompress(compressed_json, zlib.MAX_WBITS | 16)
    print ("décompression terminée avec %s"%megas(len(uncompressed_json)))

    # nous avons a ce stade une entree json par ligne
    print ("Décodage json ...")
    areas = {}
    all_cities = [ json.loads(line) for line in uncompressed_json.split("\n") if line ]
    areas ['all'] = all_cities
    print (40*'=')

    # on filtre les entrees qui correspondent a notre aire d'interet
    for areaname in filenames:
        if areaname == 'all':
            cities = all_cities
        else:
            cities = [ entry for entry in all_cities 
                       if in_area ( xpath (entry, ('city','coord')), regions[areaname] ) ]
            areas[areaname]=cities
        print ("nous avons {} villes dans la zone '{}'".format(len(cities),areaname))
        filename = filenames[areaname]
        with open(filename,"w") as output:
            output.write (json.dumps(cities))
        print ("(Over)wrote {}".format(filename))
    return areas
        
def find_data (areaname):
    filename = filenames [areaname]
    try:
        with open (filename) as input:
            return json.loads(input.read())
    except:
        areas = fetch_data ()
        return areas[areaname]

def inspect_data (cities):
    city = cities [0]

    pprint.pprint (city)

    def nb_mesures (city): return len(city['data'])
    print ("sample city has {} measurement points".format(nb_mesures(city)))

    total_mesures = sum ( [ nb_mesures(city) for city in cities ] )
    extrapolated = nb_mesures (city) * len(cities)
    print ("there are a total of {} mesures (extrapolated was {})"\
           .format(total_mesures,extrapolated))

from argparse import ArgumentParser
def main():
    parser = ArgumentParser()
    parser.add_argument("filename",help="input JSON file - might be gzipped")
    args = parser.parse_args()
    cities = load_cities(args.filename)
    if not cities:
        print ("Cannot open input {}".format(args.filename))
        return 1
    print (40*'=', 'cities ready')
    show_sample_city(cities[0])

if __name__ == '__main__':
    main()
