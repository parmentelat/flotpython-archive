# -*- coding: cp1252 -*-

## Comment manipule-t-on des objets en Python ?
## On utilise l'affectation (typage dymamique).
## On dit que l'on affecte un nom à un objet ou que
## le nom référence l'objet. Parler du typage dynamique.

a = 1 + 2
b = a + 2

## Comment affiche-t-on un objet en Python ?
## On utilise print (on peut séparer les variables
## par des virgules).

print a
print a, b

## Qu'est-ce que la représentation interne d'un objet ?
## Souvent équivallent à print (mais pas toujours).
## La représentation internet peut donner des informations
## supplémentaires.

a  #il faut taper "a" (sans les guillemets) dans l'interpréteur
   #pour voir la représentation interne

## Comment on connait le type d'un objet en Python ?
## On utilise la fonction built-in type()

type(a)

## Les types numériques

## Les entiers
i = 10
l = 23480284028402840289482184018 # précision illimitée
print l * l     # précision illimitée sur les long

type(i + l)     # conversion automatique en long si on a besoin de plus de
                # précision qu'un int

## Les décimaux. On sépare la partie entière et décimale par un .
f = 4.3
c = 1 + 3j

print f, c, c.real, c.imag


## Par contre on peut perdre en précision.
## Un int et un long donne toujours un long
## Un type entier (int, long) et un float donne toujours un float
## Un type entier (int, long) ou un float et un complex
## donne toujours un complex

print i + l
type(i+l)

print i + l + f
print type(i + l + f)

print i + l + f + c
print type(i + l + f + c)

## opérations de base

print 5 + 3
print 5 - 3
print -3
print 5/3       # division entière
print 5%3       # reste de la division entière
print 5/3.0     # division sur des floats
print 5.2//3.1  # force la division sur des entiers (5.0/3.0)
print 2 ** 32   # puissances
print abs(-5.3) # valeur absolue

## On peut convertir des types de bases entre eux (avec risque
## de perte d'information)

print int(4.32)
print long(5.3)
print float(9879729572895792375948)
print complex(10)

## Finissons par les bool

a = True
b = False

print a, b

