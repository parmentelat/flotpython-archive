#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import random

from string import Template

class Kml():

    random_inited = False
    
    def __init__(self):
        if not self.random_inited:
            random.seed(0)
            self.random_inited = True

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

                 
