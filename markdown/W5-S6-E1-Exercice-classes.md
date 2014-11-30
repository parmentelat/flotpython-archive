
# Exercice sur l'utilisation des classes

### Introduction

##### Objectifs de l'exercice

Maintenant que vous avez un bagage qui couvre toutes les bases du langage, cette
semaine nous ne ferons qu'un seul exercice de taille un peu plus réaliste. Vous
devez écrire quelques classes, que vous intégrez ensuite dans un code écrit pas
nos soins.

L'exercice comporte donc autant une part lecture qu'une part écriture. Vous êtes
également incités à améliorer autant que possible votre environnement de travail
sur votre ordinateur.

##### Objectifs de l'application

Dans le prolongement des exercices de la semaine 3 sur les données maritimes,
l'application dont il est question ici fait principalement ceci&nbsp;:
 * agréger des données obtenues auprès de marinetraffic,
 * et produire en sortie
   * un fichier texte qui liste par ordre alphabétique les bateaux concernés, et
le nombre de positions trouvées pour chacun,
   * et un fichier KML, pour exposer les trajectoires trouvées à google earth,
maps ou autre outil similaire.

Voici à quoi ressemble le fichier KML obtenu avec les données que nous
fournissons, une fois ouvert sous google earth&nbsp;:

<img src="media/ships-in-earth.png">

##### Choix d'implémentation

En particulier, dans cet exercice nous allons voir comment on peut gérer des
données sous forme d'instances de classes plutôt que de types de base. Ce qui
résonne avec la discussion commencée en Semaine 3, Séquence "Les dictionnaires",
dans le complément "record-et-dictionnaire".

Dans les exercices de cette semaine-là nous avions uniquement utilisé des types
'standard' comme listes, tuples et dictionnaires pour modéliser les données,
dans cette application nous allons faire le choix inverse et utiliser plus
souvent des (instances de) classes.

##### Correction

L'application vient avec son propre système de vérification; c'est-à-dire qu'une
fois les fichiers produits, ils sont comparés avec le résultat de
l'implémentation de référence.

Du coup le fait de disposer de google earth sur votre ordinateur n'est pas
strictement nécessaire, on ne s'en sert pas pour l'exercice.

***

### Mise en place

##### Partez d'un directory vierge

Pour commencer créez-vous un répertoire pour travailler à cet exercice

##### Les données

Commencez par y installer les donneés que nous publions dans les formats
suivants&nbsp;:
 * [format tar](data/ships-json.tar)
 * [format tgz](data/ships-json.tgz)
 * [format zip](data/ships-json.zip)

Une fois installées, ces données doivent se trouver dans un sous-répertoire
[json/] qui contient 133 fichiers

    2013-10-01-00-00--t=10--ext.json
    ...
    2013-10-01-23-50--t=10.json

Comme vous pouvez le deviner il s'agit de données sur le mouvement des bateaux
dans la zone en date du 10 Octobre 2013; et comme vous le voyez également on a
quelques exemplaires de données étendues, mais dans la plupart des cas il s'agit
de données abrégées.

##### Les résultats de référence

De même il vous faut installer les résultats de référence que vous trouvez
ici&nbsp;:
 * [format tar](data/ships-ref.tar)
 * [format tgz](data/ships-ref.tgz)
 * [format zip](data/ships-ref.zip)

ce qui vous doit vous donner trois fichiers

    ALL_SHIPS.kml.ref
    ALL_SHIPS.txt.ref
    ALL_SHIPS-v.txt.ref


### xxx niveaux de difficulté à définir if time permits

Prendre le `main` et choisir quels fichiers on veut écrire

##### Comment lancer l'application

Lorsque le programme est complet, on le lance comme ceci&nbsp;:

    $ python merger.py json/*
    Opening ALL_SHIPS.txt for listing all named ships
    Opening ALL_SHIPS.kml for ship ALL_SHIPS
    Comparing ALL_SHIPS.txt and ALL_SHIPS.txt.ref -> OK
    Comparing ALL_SHIPS.kml and ALL_SHIPS.kml.ref -> OK

qui comme on le voit produit

 * `ALL_SHIPS.txt` qui résume, par ordre alphabétique les bateaux qu'on a
trouvés et le nombre de positions pour chacun, et
 * `ALL_SHIPS.kml` qui est le fichier au format `KML` qui contient toutes les
trajectoires.

##### Comment est structurée l'application

Le point d'entrée s'appelle, donc, `merger.py`

Il utilise trois autres modules annexes, qui sont

 * `shipdict.py`, qui implémente les classes
   * `Position` qui contient une latitude, une longitude, et un timestamp,
   * `Ship` qui modélise un bateau `partir de son `id` et optionnellement un
`name` et `country`
   * `ShipDict`, qui maintient un index des bateaux (essentiellement un
dictionnaire
 * `compare.py` qui implémente
   * la classe `Compare` qui se charge de comparer les fichiers résultat avec
leur version de référence,
 * `kml.py` qui implémente
   * la classe `KML` dans laquelle sont concentrées les fonctions liées à la
génération de KML.
