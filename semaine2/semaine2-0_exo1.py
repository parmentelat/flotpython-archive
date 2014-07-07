# -*- coding: cp1252 -*-

## Comment manipule-t-on des objets en Python ?
## On utilise l'affectation (typage dymamique).
## On dit que l'on affecte un nom à un objet ou que
## le nom référence l'objet. Parler du typage dynamique.

# abcdefghijklmnopqrstuvwxyz0123456789_
prix_articles = 10

## on ne commence pas par un chiffre

1prix = 10

## on ne met pas de caractères accentués dans un nom de variable

carré_val = 8

## types de base en python
val_int = 1
val_float = 3.5 # attention, la virgule décimale est un point un Python
val_str = 'une chaine'
val_list = [] # une liste vide, suite quelconque d'éléments indexés de 0 à n-1
val_list = [val_int, val_float, val_str]

print val_list[0] # premier élément de la liste
print val_list[2]

## la liste est une structure de donnée très puissante et au coeur
## de tous les programmes Python. On verra plus tard cette semaine
## toutes les possibilités que l'on a avec une liste

