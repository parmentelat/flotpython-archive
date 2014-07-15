# -*- coding: latin_1 -*-

## On va voir dans cette vidéo les 5 types numériques en Python, les types entier
## int et long, le type décimal float, le type complex pour les nombres complexes
## et le type bool pour le booleens. 

## le type entier
## pour entrer un entier, on n'a rien d'autre à faire que d'écrire
## cet entier
1

## on peut également l'affecter à une variable
i = 1

## Comment affiche-t-on un objet en Python ?
## On utilise print (on peut séparer les variables
## par des virgules).

print i

## lorsque l'on est dans le terminal interactif, on peut aussi directement
## taper le nom de la variable suivi d'un retour chariot.

i

## On voit ainsi la représentation interne de l'objet ?
## c'est souvent équivallent à print (mais pas toujours).
## La représentation internet peut donner des informations
## supplémentaires.

## Comment on connait le type d'un objet en Python ?
## On utilise la fonction built-in type()

type(i)

## en python on a deux type entiers, les int et les long
i = 10
l = 23480284028402840289482184018 # précision illimitée
print l * l     # précision illimitée sur les long

## pourquoi avons nous deux types entier en Python ?
## le type int est plus compact que le type long, par conséquent
## pour les petits entier, Python va utiliser le type int pour reduire
## la consommation mémoire, et le type long s'il y a vraiement besoin de
## grands entiers.

## heureusement, Python fait automatiquement la conversion
## de int vers long s'il y a besoin. Donc en pratique vous n'avez
## jamais à vour préocupé du type d'entier que vous utilisez

type(i + l)     

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
## de perte de précision ou d'information, troncation).

print int(4.32)
print long(5.3)
print float(9879729572895792375948)
print complex(10)

## Finissons par les bool

a = True
b = False

print a, b

