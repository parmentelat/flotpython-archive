# -*- coding: cp1252 -*-

## On va voir dans cette vidéo 4 types de base en Python, le type entier
## le type décimal, le type chaîne de charactères et le type liste.

## le type entier
## pour entrer un entier, on n'a rien d'autre à faire que d'écrire
## cet entier et de l'affecter à une variable
val_int = 1

## le type décimal
val_float = 3.5 # attention, la virgule décimale est un point un Python

## pour afficher la valeur d'un objet référencé par une variable,
## on utilise l'instruction print

print val_int

## on a les opérations numériques classiques sur les types numériques
##(c'est-à-dire entier et decimal) et Python fait automatiquement
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

print 'spam' + 'egg'

print [1, 2] + [3, 4]

## la liste est une structure de donnée très puissante et au coeur
## de tous les programmes Python. On verra plus tard cette semaine
## toutes les possibilités que l'on a avec une liste

## 3 minutes 30 secondes

## maintenant que nous avons introduit certains types de base, j'aimerai
## vous parler d'une intruction très importante qui permet d'exécuter ou
## de ne pas executer une portion de code en fonction d'une condition,
## c'est l'instruction if elif else. Passons maintenant dans un éditeur de texte...

