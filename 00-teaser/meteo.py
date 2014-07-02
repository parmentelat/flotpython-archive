#!/usr/bin/env python
# -*- coding: cp1252 -*-

import sys
import types
import time
# izip plutot que zip
import itertools
# une librairie pour les noms de fichier
import os.path
# une librairie pour decharger des donnees au dessus de http
import urllib2
# une librairie pour decompresser le format .gz
import zlib
# une librairie pour decortiquer le format json
import json

# pour la visualisation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

date_format="%Y-%m-%d:%H-%M"

# chercher par exemple entry['city']['id'] a partir d'un chemin genre ('city','id')
# i.e. xpath ( {'city':{'id':12,'name':'Montreal'}}, ['city','id']) => 12
def xpath (entry, path):
    result=entry
    for key in path:
        result=result[key]
    return result

# on a des megas...
def megas(bytes):
    megas=float(bytes)/1024**2
    megas=float(int(megas*10))/10
    return "%s Mo"%megas

#################### peut-etre pas utile
# aller chercher les donnees a une url et les decompresser 
# ou les prendre dans le cache s'il exite
def fetch_compressed_data (url,cache):
    print "Téléchargement de %s ..."%url,
    sys.stdout.flush()
    network_file=urllib2.urlopen(url)
    compressed_json=network_file.read()
    print " OK - %s "%megas(len(compressed_json))
    uncompressed_json=zlib.decompress(compressed_json, zlib.MAX_WBITS | 16)
    print "décompression terminée avec %s"%megas(len(uncompressed_json))
    return uncompressed_json

# like in css we do: top right bottom left
france = ( 50, 8, 42, -5)
europe = ( 60, 26, 34, -12)

# determiner si une position est dans un rectangle donne
def in_area ( lat_lon_rec, css_4uple):
    (top, right, bottom, left)=css_4uple
    lon=lat_lon_rec['lon']
    lat=lat_lon_rec['lat']
    return lon>=left and lon<=right and lat>=bottom and lat<=top

def main ():
    
    print 40*'='
    url = "http://78.46.48.103/sample/daily_14.json.gz"

    print "Téléchargement de %s ..."%url
    network_file=urllib2.urlopen(url)
    compressed_json=network_file.read()
    print "OK - %s téléchargés"%megas(len(compressed_json))
    uncompressed_json=zlib.decompress(compressed_json, zlib.MAX_WBITS | 16)
    print "décompression terminée avec %s"%megas(len(uncompressed_json))

    print "Décodage json ...", 
    sys.stdout.flush()
    # nous avons a ce stade une entree json par ligne
    all_entries = [ json.loads(line) for line in uncompressed_json.split("\n") if line ]
    print "OK"
    print "nous avons %s entrées de ville"%len(all_entries)

    print 40*'='
    print("téléchargement terminé..")
    print 40*'='

    # on filtre les entrees qui correspondent a notre aire d'interet
    entries_in_europe = [ entry for entry in all_entries 
                        if in_area ( xpath (entry, ('city','coord')), europe ) ]
    print "nous avons %s villes dans la zone 'europe'"%len(entries_in_europe)

    entries_in_france = [ entry for entry in all_entries 
                        if in_area ( xpath (entry, ('city','coord')), france ) ]
    print "nous avons %s villes dans la zone 'france'"%len(entries_in_france)

    # visualiser l'ensemble des positions lon/lat
    print "Les points de relèvement en France par rapport à l'Europe"
    LON_s = [ entry['city']['coord']['lon'] for entry in entries_in_europe ]
    LAT_s = [ entry['city']['coord']['lat'] for entry in entries_in_europe ]
    # mettre une taille et une couleur particuliere pour ceux qu'on a retenus
    for entry in entries_in_france: entry['selected']=True
    # les entrées dans la zone d'intérêt en rouge
    colors = [ 'r' if  'selected' in entry else 'b' for entry in entries_in_europe ]
    # et un peu plus grosses
    sizes = [ 30 if 'selected' in entry else 1 for entry in entries_in_europe ]
    plt.scatter(LON_s, LAT_s, c=colors, s=sizes)

    print 40*'='
    plt.show()

    # pour faire simple on va visualiser la pression observee dans la zone le premier jour
    day=0
    dt=xpath(entries_in_france[0],('data',day,'dt'))
    date=time.strftime(date_format,time.localtime(dt))
    print "Visualisation de la pression observée le ",date
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = [ xpath (entry, ('city','coord','lon')) for entry in entries_in_france ]
    Y = [ xpath (entry, ('city','coord','lat')) for entry in entries_in_france ]
    P = [ xpath (entry, ('data',day,'pressure')) for entry in entries_in_france ]
    ax.plot_trisurf(X,Y,P, cmap=cm.jet, linewidth=0.2, label="Pression le %s"%date)
    ax.set_title ("Pression en France relevee le %s"%date)

    print 40*'='
    plt.show()

if __name__ == '__main__': main()
