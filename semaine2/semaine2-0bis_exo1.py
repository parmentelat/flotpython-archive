# -*- coding: cp1252 -*-

## types de base en python
## les types numériques
val_int = 1
val_float = 3.5 # attention, la virgule décimale est un point un Python

## on a les opérations numériques classiques, Python fait automatiquement
## les convertions si nécessaire

print val_int + val_float
print val_int - val_float
print val_int * val_float
print val_int / val_float

## le type chaîne de catactères
val_str = 'une chaine'

## le type liste
val_list = [] # une liste vide, suite quelconque d'éléments indexés de 0 à n-1
val_list = [val_int, val_float, val_str]

print val_list[0] # premier élément de la liste
print val_list[2]

## l'opérateur + est définit pour les chaînes de caractères et les listes
## il retourne un nouvel objet de même type qui est la concaténation
## des deux objets initiaux

print 'spam' + 'ham'

print [1, 2] + [3, 4]

## la liste est une structure de donnée très puissante et au coeur
## de tous les programmes Python. On verra plus tard cette semaine
## toutes les possibilités que l'on a avec une liste

