
# Visualisation de données météo

## Mini-Projet

### Introduction

Ce mini-projet vise à vous donner accès à des données assez riches pour vous
permettre d'expérimenter avec `matplotlib`, et mettre en oeuvre une
visualisation de données en 2D et en 3D.

Nous allons pour cela travailler avec des données obtenues auprès de
[OpenWeatherMap](https://openweathermap.desk.com).

Spécifiquement, ce site publie un échantillon statique de données qui est
disponible à cette URL

    http://78.46.48.103/sample/daily_14.json.gz

L'échantillon couvre le monde entier et expose des données météo sur une période
d'environ deux semaines en Mars 2014.

### Les données

Une fois décompressé et décodé, l'échantillon contient, pour un grand nombre de
villes (22631 exactement), des données de type&nbsp;:
 * champ `city` : position géographique, nom, etc..
 * champ `time` : date (vous pouvez ignorer ce champ pour l'exercice)
 * champ `data` : une liste de mesures disponibles concernant ce point, sous la
forme d'une liste de mesures; l'échantillon contient en moyenne 16 mesures par
point;
 * élément de `data` : une mesure correspond à un jour donné, et vient comme un
dictionnaire contenant typiquement une valeur pour
   * l'heure des mesures (champ `dt`, pour data time) - voir aussi plus bas,
   * la vitesse et la direction du vent (`speed` et `deg`)
   * l'humidité et la pression
   * et s'agissant de la température, à nouveau un dictionnaire pour décrire les
températures à divers moments de la journée

Je vous laisse deviner les unités utilisées - je rappelle juste que

$ 0°C = 273.15°K $


Pour être plus explicite encore, voici un pretty-print d'un objet correspondant
à une ville (Cayenne en Guyanne), en ne montrant que la première mesure&nbsp;:

                {u'city': {u'coord': {u'lat': 49.558578, u'lon': 1.62803},
           u'country': u'FR',
           u'id': 3028097,
           u'name': u'Cayenne'},
 u'data': [{u'clouds': 80,
            u'deg': 330,
            u'dt': 1394884800,
            u'humidity': 85,
            u'pressure': 1028.47,
            u'speed': 5.41,
            u'temp': {u'day': 282.3,
                      u'eve': 282.86,
                      u'max': 283.22,
                      u'min': 279.7,
                      u'morn': 279.7,
                      u'night': 281.96},
            u'weather': [{u'description': u'broken clouds',
                          u'icon': u'04d',
                          u'id': 803,
                          u'main': u'Clouds'}]},
           '... other similar dicts ...'],
 u'time': 1394865585}
                
##### Rappel sur les dates

S'agissant des dates, on retrouve ici notre nombre de secondes depuis le
$1^{er}$ Janvier 1970, et voici comment vous pouvez afficher ce genre de
valeurs.


    import time
    # *Y*ear *m*onth *d*ay *H*our *M*inute
    date_format="%Y-%m-%d:%H-%M UTC"
    
    # city['city']['data'][0]['dt']
    dt = 1394884800
    
    # gmtime pour afficher en heure UTC (formerly GMT)
    print 'champ dt', time.strftime(date_format, time.gmtime(dt))


### Mise en place

Comme l'échantillon est très gros, je vous ai préparé des versions de plus en
plus petites&nbsp;:

 * Monde entier (échantillon complet)
   * [cities_world.json.gz](data/cities_world.json.gz) (11 Mb)
   * [cities_world.json](data/cities_world.json) (98 Mb)
 * Europe (62, 33, 34, -11) (limites nord, est, sud, et ouest)
   * [cities_europe.json.gz](data/cities_europe.json.gz) (3 Mb)
   * [cities_europe.json](data/cities_europe.json) (31 Mb)
 * France (51.2, 8.3, 42.3, -5.3)
   * [cities_france.json.gz](data/cities_france.json.gz) (480 kb)
   * [cities_france.json](data/cities_france.json) (6 Mb)
 * Ile-de-France (49, 2.75, 48.5, 2)
   * [cities_idf.json.gz](data/cities_idf.json.gz) (17 kb)
   * [cities_idf.json](data/cities_idf.json) (900 kb)

Sachant que pour mette au point il est très conseillé de commencer avec un petit
fichier.

##### 

Plot 2D

http://matplotlib.org/api/pyplot_api.html?highlight=scatter
