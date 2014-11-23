
# Premiers pas avec des données météo

xxx - à reprendre

## Exercice - niveau intermédiaire

Nous allons à présent travailler avec des données obtenues auprès de
[OpenWeatherMap](https://openweathermap.desk.com) à cette URL
http://78.46.48.103/sample/daily_14.json.gz - en fait un sous-ensemble de
celles-ci pour des raisons de taille.

Nous verrons plus tard comment on aurait pu utiliser python pour nous procurer
ces données directement auprès de OpenWeatherMap, mais pour le moment
contentons-nous d'utiliser une copie locale; vous avez dès maintenant accès à un
fichier qui s'appelle `data/meteo_france.json`.

Ici encore nous utilisont le module [module
`json`](https://docs.python.org/2/library/json.html) pour charger ces données en
mémoire.


    # le module json
    import json
    
    # chargement des données au format json
    with open('data/meteo_france.json') as feed:
        raw_data = all_cities = json.load(feed)


    city=raw_data[0]
    import pprint
    pprint.pprint(city)


    print city.keys()


    city['time']

                
                