#!/usr/bin/env python

import sys
import types
import time
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

daily14_url = "http://78.46.48.103/sample/daily_14.json.gz"
daily14_cache = "daily_14.json.cache"

upper_left_lat_lon = ( 50, -5)
lower_right_lat_lon = (42, 8)

date_format="%Y-%m-%d:%H-%M"

# chercher par exemple entry['city']['id'] a partir d'un chemin genre ('city','id')
# i.e. xpath ( {'city':{'id':12,'name':'Montreal'}}, ['city','id']) => 12
def xpath (entry, path):
    result=entry
    for key in path:
        result=result[key]
    return result

#################### peut-etre pas utile
# calculer un hash de toutes les entrees par une cle obtenue a partir d'un chemin
# e.g. 
# entries = [ {'city':{'name':'Grenoble'},'data':data1}, {'city':{'name':'Toulouse'},'data':data2} ]
# path = ('city','name')
# result = { 'Grenoble': [ {'city':{'name':'Grenoble'},'data':data1}],
#            'Toulouse': [ {'city':{'name':'Toulouse'},'data':data2} ],
# }
def hash_by_path (entries, path):
    result = {}
    for entry in entries:
        key=xpath(entry,path)
        if key not in result: result[key]=[]
        result[key].append(entry)
    return result
#################### peut-etre pas utile

# aller chercher les donnees a une url et les decompresser 
# ou les prendre dans le cache s'il exite
def fetch_compressed_data (url,cache):
    if os.path.isfile(cache):
        # il faudrait verifier la date de ce cache..
        print '%s: on utilise le cache %s'%(url,cache)
        with open(cache) as f: 
            return f.read()
    print 'Telechargement de %s ...'%url,
    sys.stdout.flush()
    network_file=urllib2.urlopen(url)
    compressed_json=network_file.read()
    print ' OK - %s octets'%len(compressed_json)
    # http://stackoverflow.com/questions/3122145/zlib-error-error-3-while-decompressing-incorrect-header-check
    uncompressed_json=zlib.decompress(compressed_json, zlib.MAX_WBITS | 16)
    print "decompression terminee"
    with open(cache,'w') as f:
        print '%s: on sauve dans le cache %s'%(url,cache)
        f.write(uncompressed_json)
    return uncompressed_json

# determiner si une position est dans un rectangle donne
def in_area ( lat_lon_rec, upper_left_lat_lon, lower_right_lat_lon):
    (upper,left)=upper_left_lat_lon
    (lower,right)=lower_right_lat_lon
    lon=lat_lon_rec['lon']
    lat=lat_lon_rec['lat']
    return lon>=left and lon<=right and lat>=lower and lat <= upper

# enchainer le tout
def main ():
    raw_daily14 = fetch_compressed_data (daily14_url, daily14_cache)
    print 'Parsing json ...', 
    sys.stdout.flush()
    # nous avons a ce stade une entree json par ligne
    all_entries = [ json.loads(line) for line in raw_daily14.split("\n") if line ]
    print 'OK, nous avons %s entrees'%len(all_entries)
    
    # on filtre les entrees qui correspondent a notre aire d'interet
    entries_in_area = [ entry for entry in all_entries 
                        if in_area ( xpath (entry, ('city','coord')), 
                                     upper_left_lat_lon, lower_right_lat_lon) ]
    print 'nous avons %s entrees dans la zone'%len(entries_in_area)

    # xxx on pourrait filtrer sur un autre critere comme un RE pour le nom de la ville...
    # a voir

    # creer une table de hash sur le nom de la ville
    hash_by_city_name = hash_by_path (entries_in_area, ('city','name'))
    print 'nous avons %s noms de villes differents'%len(hash_by_city_name)

    # grouper les entrees par l'initiale du nom, afficher une ville par entree
    hash_by_first_letter = hash_by_path (entries_in_area, ('city', 'name', 0))
    for letter in [ str(chr(ord('A')+i)) for i in xrange(26) ]:
        try: 
            entry=hash_by_first_letter[letter][0]
            print letter,':',entry['city']['name'],'...'
        except: 
            # pas de ville commencant par cette lettre
            pass

    # montrer les villes qui font l'objet de plusieurs entrees
    duplicates = [ (name,l) for (name,l) in hash_by_city_name.iteritems() if len(l) >=2 ]
    for (name,l) in duplicates:
        print "DUP: ",name

#    # afficher une entree echantillon
#    # chaque entree a un champ 'city' qui decrit le point de mesures
#    # et un champs 'data' qui contient une liste de cellules
#    # et chaque cellule correspond a un ensemble de mesures a cet instant et a cet endroit
#    import pprint
#    pp=pprint.PrettyPrinter()
#    entry=entries_in_area[0]
#    print 10*'=',"sample data for",xpath(entry,('city','name'))
#    print 4*'=',"entry['city']"
#    pp.pprint(entry['city'])
#    print 4*'=',"entry['data'][0]"
#    pp.pprint(entry['data'][0])
#    print 4*'=',"entry"
#    pp.pprint(entry)

    # visualisation 
    # pour faire simple on va visualiser la pression observee dans la zone le premier jour
    # en admettant que tous les tableaux de 'data' sont synchrones
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = [ xpath (entry, ('city','coord','lon')) for entry in entries_in_area ]
    Y = [ xpath (entry, ('city','coord','lat')) for entry in entries_in_area ]
    for day in 0,: # seulement le premier jour
        date = time.strftime(date_format,time.localtime(entries_in_area[0]['data'][day]['dt']))
        print 'echantillon du ',date
        P = [ xpath (entry, ('data',day,'pressure')) for entry in entries_in_area ]
        ax.plot_trisurf(X,Y,P, cmap=cm.jet, linewidth=0.2, label="Pression le %s"%date)
    plt.show()

if __name__ == '__main__': main()
