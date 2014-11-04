
# Fusionner des données

## Exercice - niveau intermédiaire

### Contexte

Nous allons commencer à utiliser des données un peu plus réalistes. Il s'agit de
données obtenues auprès de [MarineTraffic](https://www.marinetraffic.com) - et
légèrement simplifiées pour les besoins de l'exercice. Ce site expose les
coordonnées géographiques de bateaux observées en mer au travers d'un réseau de
collecte de type *crowdsourcing*.

De manière à optimiser le volume de données à transférer, l'API de MarineTraffic
offre deux modes pour obtenir les données
 * **mode étendu** : chaque mesure (bateau x position x temps) est accompagnée
de tous les détails du bateau (`id`, nom, pays de rattachement, etc..)
 * **mode abrégé** : chaque mesure est uniquement attachée à l'`id` du bateau.

En effet, chaque bateau possède un identifiant unique qui est un entier, que
l'on note  `id`.

### Chargement des données

Nous allons travailler avec une copie locale de ces données; vous avez dès
maintenant accès aux deux fichiers
 * `data/marine-e1-ext.json` - données étendues
 * `data/marine-e1-abb.json` - données abrégées

Pour charger ces fichiers qui sont au [format
JSON](http://en.wikipedia.org/wiki/JSON), la connaissance intime de ce format
n'est pas nécessaire, nous allons utiliser le [module
`json`](https://docs.python.org/2/library/json.html). Vous pouvez utiliser la
cellule qui suit telle quelle, ces détails ne font pas partie de l'exercice
parce que cette cellule utilise des notions que nous verrons dans les semaines à
venir.


    # load data from files
    import json
    
    with open("data/marine-e1-ext.json") as feed:
        extended = json.load(feed)
        
    with open("data/marine-e1-abb.json") as feed:
        abbreviated = json.load(feed)

### Format des données

Le format de ces données est relativement simple, il s'agit dans les deux cas
d'une liste d'entrées - une par bateau.

Chaque entrée à son tour est une liste qui contient :

    mode étendu: [id, latitude, longitude, date_heure, nom_bateau, code_pays,
...]
    mode abrégé: [id, latitude, longitude, date_heure]

sachant que les entrées après le code pays dans le format étendu ne nous
intéressent pas pour cet exercice.


    # une entrée étendue est une liste qui ressemble à ceci
    print extended[7]


    # une entrée abrégée ressemblent à ceci
    print abbreviated[0]

On précise également que les deux listes `extended` et `abbreviated` possèdent
exactement **le même nombre** d'entrées et correspondent **aux mêmes bateaux** -
mais naturellement à des moments différents.

### But de l'exercice

On vous demande d'écrire une fonction `merge` qui fasse une consolidation des
données, de façon à obtenir en sortie un dictionnaire:

    id -> [ nom_bateau, code_pays, position_etendu, position_abrege ]

dans lequel les deux objets `position` sont tous les deux des tuples de la forme

    (latitude, longitude, date_heure)

Voici par exemple un couple clé-valeur dans le résultat attendu. Profitons-en
pour découvrir un utilitaire parfois pratique: le [module `pprint` pour pretty-
printer](https://docs.python.org/2/library/pprint.html)


    # le résultat attendu
    from corrections.w3_marine_dict import exo_merge
    result = exo_merge.resultat(extended, abbreviated)
    
    # a quoi ressemble le résultat pour un bateau au hasard
    from pprint import pprint
    for key_value in result.iteritems():
        pprint(key_value)
        break

### Votre code


    def merge(extended, abbreviated):
        "<votre_code>"

### Validation


    exo_merge.correction(merge, extended, abbreviated)
