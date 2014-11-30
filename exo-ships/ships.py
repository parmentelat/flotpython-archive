#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

class Position(object):
    "a position atom with timestamp attached"
    def __init__(self, latitude, longitude, timestamp):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    @staticmethod
    def _lat_str(f):
        if f>=0:        return "{}°N".format(f)
        else:           return "{}°S".format(-f)
    
    @staticmethod
    def _lon_str(f):
        if f>=0:        return "{}°E".format(f)
        else:           return "{}°W".format(-f)
        
    def lat_str(self):  return self._lat_str(self.latitude)
    def lon_str(self):  return self._lon_str(self.longitude)

    def __repr__(self):
        return "<{} {} @ {}".format(self.lat_str(), self.lon_str(), self.timestamp)


class Ship(object):
    """
    a ship object, that also has a list of known positions
    """
    def __init__(self, id, name=None, country=None):
        self.id = id
        self.name = name
        self.country = country
        # this is where we remember the various positions over time
        self.positions = []

    def add_position(self, position):
        self.positions.append(position)

    def sort(self):
        """sort list of positions by chronological order"""
        # xxx - fixme - this is probably very wrong
        self.positions.sort()

    def print(self):
        print (40*'-', "Ship:{} ({})".format(self.name, self.country))
        for position in self.positions:
            print (position)
        
class ShipDict(dict):
    """
    a repository for storing all ships that we know about
    indexed by their id
    """
    def __init__(self):
        dict.__init__(self)

    def __repr__(self):
        return "<ShipDict instance with {} ships>".format(len(self))

    @staticmethod
    def is_abbreviated(chunk):
        """
        depending on the size of the incoming data chunk, 
        guess if it is an abbreviated or extended data
        """
        return len(chunk) <= 7

    def add_abbreviated(self, chunk):
        id, latitude, longitude, _, _, _, timestamp = chunk
        # xxx improve me - setdefault could work but would create an object each time
        if id not in self:
            self[id] = Ship(id)
        ship = self[id]
        ship.add_position (Position (latitude, longitude, timestamp))
        
    def add_extended(self, chunk):
        id, latitude, longitude = chunk[:3]
        timestamp, name = chunk[5:7]
        country = chunk[10]
        if id not in self:
            self[id] = Ship(id)
        ship = self[id]
        if not ship.name:
            ship.name = name
            ship.country = country
        self[id].add_position (Position (latitude, longitude, timestamp))

    def add_chunk(self, chunk):
        if self.is_abbreviated(chunk):
            self.add_abbreviated(chunk)
        else:
            self.add_extended(chunk)

    def sort(self):
        for id, ship in self.iteritems():
            ship.sort()

#    def list_names(self):
#        all_ship_names = [ ship.name for ship in self.values() ]
#        all_ship_names.sort()
#        for name in all_ship_names:
#            print (name)

    def ships_by_name(self, name):
        """
        returns a list of all known ships with name <name>
        """
        return [ ship for ship in self.values() if ship.name == name ]

    def all_ships(self):
        return self.values()

    def clean_unnamed(self):
        """
        Because we enter abbreviated and extended data in no particular order,
        we might have ship instances with no name attached
        This method removes such entries from the dict
        """
        unnamed_ids = { id for id, ship in self.iteritems() if ship.name is None }
        for id in unnamed_ids:
            del self[id]

##############################            
import random

from string import Template

class KmlOutput():
    def __init__(self):
        pass

    def normalize (self, name):
        return name.replace("&","")
    
    def random_color(self):
        """
        as per https://developers.google.com/kml/documentation/kmlreference#color
        a KML color is aabbggrr - essentially the exact opposite of what you would expect
        we set alpha = 80 (128) and compute the other 3 in the 10-245 range
        """
        colors = [128] + [random.randint(10,245) for i in range(3)]
        return "".join(["{:02x}".format(c) for c in colors])

    def ship_trip(self, ship):

        coordinates = "\n".join(["{},{},0".format(position.longitude, position.latitude)
                                 for position in ship.positions])

        # https://developers.google.com/kml/documentation/kml_tut#paths
        template = Template ("""
    <Placemark>
      <name>$ship_normal_name</name>
      <description>Known positions for ship $ship_normal_name</description>
      <styleUrl>#style_$ship_normal_name</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates> $coordinates
        </coordinates>
      </LineString>
    </Placemark>
""")
        return template.substitute(ship_normal_name=self.normalize(ship.name),
                                   coordinates=coordinates)

    def ship_style (self, ship):
        template = Template("""<Style id="style_$ship_normal_name">
      <LineStyle>
        <color>$color</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>ff000088</color>
      </PolyStyle>
    </Style>""")
        return template.substitute(ship_normal_name=self.normalize(ship.name),
                                   color=self.random_color())
        
    def contents (self, global_name, description, ships):

        styles = "".join([self.ship_style(ship) for ship in ships])
        
        placemarks = "".join([self.ship_trip(ship) for ship in ships])
        
        # https://developers.google.com/kml/documentation/kml_tut#paths
        template = Template( # must start on line 1
"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>$global_name</name>
    <description>$description</description>
  $styles
  $placemarks
  </Document>
</kml>
""")
        return template.substitute(global_name=global_name, description=description,
                                   placemarks=placemarks, styles=styles)

                 
########################################
import gzip

import json
from argparse import ArgumentParser
            
class Merger(object):
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument ("-v", "--verbose", dest='verbose', default=False, action='store_true',
                             help="Verbose mode")
        parser.add_argument ("-s", "--ship", dest='ship_name', default=None, action='store',
                             help="Select ships by that name")
        parser.add_argument ("-o", "--output", dest='output_filename', default=None, action='store',
                             help="Select output name - default is <ship_name>.kmz")
        parser.add_argument ("-z", "--gzip", dest='gzip', default=False, action='store_true',
                             help="Store output in gzip format")
        parser.add_argument ("inputs", nargs='*')
        self.args = parser.parse_args()

        self.ships = ShipDict()
        
    def merge(self, inputs):
        for json_input_filename in inputs:
            if self.args.verbose:
                print ('Opening {} for parsing JSON'.format(json_input_filename))
            with open(json_input_filename) as feed:
                chunks = json.load(feed)
                for chunk in chunks:
                    self.ships.add_chunk(chunk)
        self.ships.clean_unnamed()

    def list_ships(self, ships):
        print ("Found {} ships with name {}", len(ships))
        names = [ ship.name for ship in ships ]
        names.sort()
        for name in names: print (name)

    def main(self):
        try:
            self.merge(self.args.inputs)
            if not self.args.ship_name:
                ships = self.ships.all_ships()
                ship_name = "ALL_SHIPS"
            else:
                ship_name = self.args.ship_name
                ships = self.ships.ships_by_name(ship_name)
            self.list_ships(ships)
            kml_output = KmlOutput()
            kml_text = kml_output.contents(ship_name, "some description", ships)
            suffix = "kmz" if self.args.gzip else "kml"
            out_name = self.args.output_filename or "{}.{}".format(ship_name, suffix)
            print ("Opening {out_name} for ship {ship_name}".format(**locals()))
            with gzip.open(out_name, 'w') if self.args.gzip else open(out_name, 'w') as out:
                out.write(kml_text)
            print('Done')
            return 0
        except Exception as e:
            print ('Something went wrong',e)
            import traceback
            traceback.print_exc()
            return 1

if __name__ == '__main__':
    merger = Merger()
    exit(merger.main())
