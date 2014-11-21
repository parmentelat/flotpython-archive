
# Exercice sur les ensembles

## Exercice - niveau intermédiaire

### Chargement des données

Nous reprenons le même genre de données marines en provenance de MarineTraffic
que nous avons vues dans l'exercice précédent.


    # load data from files
    import json
    
    with open("data/marine-e2-ext.json") as feed:
        extended = json.load(feed)
        
    with open("data/marine-e2-abb.json") as feed:
        abbreviated = json.load(feed)

### Rappels sur les formats

    étendu: [id, latitude, longitude, date_heure, nom_bateau, code_pays...]
    abrégé: [id, latitude, longitude, date_heure]


    print "extended has {} entries".format(len(extended))
    print extended[12]


    print "abbreviated has {} entries".format(len(abbreviated))
    print abbreviated[0]

### But de l'exercice

Notez bien une différence importante avec l'exercice précédent: cette fois **il
n'y a plus correspondance** entre les bateaux rapportés dans les données
étendues et abrégées. On vous demande d'écrire une fonction qui retourne un
tuple à trois éléments
 * l'ensemble (`set`) des noms des bateaux présents dans `extended` mais pas
dans `abbreviated`
 * l'ensemble des noms des bateaux présents dans `extended` et dans
`abbreviated`
 * l'ensemble des `id` des bateaux présents dans `abbreviated`
 mais pas dans `extended`


    # load data from files
    import json
    
    with open("data/marine-e2-ext.json") as feed:
        extended = json.load(feed)
        
    with open("data/marine-e2-abb.json") as feed:
        abbreviated = json.load(feed)


    # le résultat attendu
    from corrections.w3_marine_set import exo_diff
    result = exo_diff.resultat(extended, abbreviated)
    
    # combien de bateaux sont concernés
    def show_result(result):
        extended_only, both, abbreviated_only = result
        print 'dans extended mais pas dans abbreviated', len(extended_only)
        print 'dans les deux', len(both)
        print 'dans abbreviated mais pas dans extended', len(abbreviated_only)
    
    show_result(result)

### Votre code


    def diff(extended, abbreviated):
        "<votre_code>"

### Validation


    exo_diff.correction(diff, extended, abbreviated)

### Debugging


    # pour utiliser ceci il faut que votre fonction renvoie un 3-tuple
    my_result = diff(extended, abbreviated)
    show_result(my_result)

### Les fichiers de données

Pour télécharger les deux fichiers de données&nbsp;:
 * [data/marine-e2-ext.json](data/marine-e2-ext.json)
 * [data/marine-e2-abb.json](data/marine-e2-abb.json)
