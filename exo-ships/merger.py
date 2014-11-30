#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from marine import Position, Ship, ShipDict

from kml import Kml

from compare import Compare

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

    def list_ships(self, ships, filename):
        print ("Opening {filename} for listing all named ships".format(**locals()))
        with open(filename, 'w') as ships_list:
            ships_list.write ("Found {} ships\n".format(len(ships)))
            dict_by_name = { ship.name : ship for ship in ships }
            for name in sorted(dict_by_name):
                ships_list.write ("{} ({} positions)\n".format(name, len(dict_by_name[name].positions)))
        return filename

    def main(self):
        try:
            self.merge(self.args.inputs)
            if not self.args.ship_name:
                ships = self.ships.all_ships()
                ship_name = "ALL_SHIPS"
            else:
                ship_name = self.args.ship_name
                ships = self.ships.ships_by_name(ship_name)

            summary_filename = "ALL_SHIPS.txt"
            self.list_ships(ships, summary_filename)

            kml = Kml()
            contents = kml.contents(ship_name, "some description", ships)
            suffix = "kmz" if self.args.gzip else "kml"
            kml_filename = self.args.output_filename or "{}.{}".format(ship_name, suffix)
            print ("Opening {kml_filename} for ship {ship_name}".format(**locals()))
            with gzip.open(kml_filename, 'w') if self.args.gzip else open(kml_filename, 'w') as out:
                out.write(contents)
            
            ok_summary = Compare(summary_filename).compare_and_print()
            ok_kml     = Compare(kml_filename).compare_and_print()
            ok         = ok_summary and ok_kml
            return 0 if ok else 1
        except Exception as e:
            print ('Something went wrong',e)
            import traceback
            traceback.print_exc()
            return 2

if __name__ == '__main__':
    merger = Merger()
    exit(merger.main())
