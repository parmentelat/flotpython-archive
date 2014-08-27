# -*- coding: iso-8859-15 -*-

## Il existe deux manières de créer un dictionnaire, la
## plus simple lorsque l'on crée un dictionnaire à la main
## est d'utiliser les accolades

d = {}

d = {'marc':35, 'alice':30, 'eric':38}

## la deuxième manière est très utile lorsque les couples
## clefs valeurs sont obtenues par une opération, dans
## ce cas on peut automatiquement créer un dictionnaire
## à partir d'une liste de tuple clef,valeur

a = [('marc', 35), ('alice', 30), ('eric', 38)]
d = dict(a)

## je rappelle qu'il n'y a pas d'ordre dans un dictionnaire
## donc le dictionnaire n'affiche pas nécéssairement
## les valeurs dans l'ordre dans lesquels on les a entré

print d

## il existe de très nombreuse opérations et fonctions
## sur les dictionnaires, nous allons voir les principales
## commençons par les deux suivantes

print len(d)
print 'marc' in d
print 'marc' not in d

## même si les dictionnaires ne sont pas des séquences,
## dans un soucis d'uniformité et de simplification,
## la fonction len et l'opérateur in ont été implémenté
## sur les dictionnaires.

## on peut accéder et modifier la valeur d'une clef de la
## manière suivante

print d['marc']
d['marc'] = 40

## on peut effacer une la clef et sa valeur dans le dictionnaire
## avec l'instruction del

del d['marc']

d.copy() # shallow copie du dictionnaire
print 

## et on a des méthodes pour récupérer les clefs dans une liste
## les valeurs dans une liste, et les tuples (clefs, valeur)
## dans une liste. 

print d.keys()
print d.values()
print d.items()
