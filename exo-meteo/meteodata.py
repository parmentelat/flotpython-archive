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
import zlib
# unmarshalling JSON data
import json

date_format="%Y-%m-%d:%H-%M"

KELVIN=273.15

filenames = { 'all': "meteo_all.json",
              'europe' : "meteo_europe.json",
              'france':  "meteo_france.json",
          }
regions = { 'france': ( 50, 8, 42, -5),
            'europe': ( 60, 26, 34, -12), }

# chercher par exemple entry['city']['id'] a partir d'un chemin genre ('city','id')
# i.e. xpath ( {'city':{'id':12,'name':'Montreal'}}, ['city','id']) => 12
def xpath (entry, path):
    result=entry
    for key in path: result=result[key]
    return result

# on a des megas...
def megas(bytes):
    megas=float(bytes)/1024**2
    megas=float(int(megas*10))/10
    return "%s Mo"%megas


# like in css we do: top right bottom left

# determiner si une position est dans un rectangle donne
def in_area ( lat_lon_rec, css_4uple):
    (top, right, bottom, left)=css_4uple
    lon=lat_lon_rec['lon']
    lat=lat_lon_rec['lat']
    return lon>=left and lon<=right and lat>=bottom and lat<=top

def fetch_data ():

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
    import pprint

    print ("Sample city")
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
    parser.add_argument("areaname",help="pick among 'all', 'europe', 'france'")
    args = parser.parse_args()
    meteo_data = find_data(args.areaname)
    print (40*'=', 'meteo_data ready')
    inspect_data(meteo_data)

main()
