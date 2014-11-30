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

    def all_ships_as_list(self):
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

