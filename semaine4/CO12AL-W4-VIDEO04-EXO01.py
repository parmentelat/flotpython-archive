# -*- coding: iso-8859-15 -*-

## créons un fichier spam.py
x = 1
def f():
    print 'x dans spam.py', x

## puis du prompt interactif jouons avec ce module
## commençons par importer 
import spam

## on peut accéder aux variables du module spam en utilisant
## la notation spam.nom, nom étant un nom de variable
print spam.x
print spam.f()

## si on crée un variable x, elle sera dans l'espace
## de nommage du prompte interactif et nom de spam
x = 10

## x dans spam vaut toujours 1
print spam.x

## Par contre, on peut modifier x dans spam
spam.x = 2

print spam.x
spam.f()

## c'est très important. Comme il n'y a qu'un seul
## objet module par module importé, par exemple
## le module spam, tous les autres modules qui importeront
## spam verrons les variables de spam modifiées.

## Regardons maintenant une autre manière d'importer un module

print x
from spam import x
print x

## avec l'instruction from, la variable x a été importé
## dans l'espace de nommage du module courant.
## Qu'est-ce que ça veut dire exactement ? On crée une
## variable locale x qui référence l'objet référencé par
## la variable spam.x, mais la variable x existe toujours
## dans l'espace de nommage de spam. On a donc maintenant
## deux variables x, une dans l'espace de nommage du module
## courant et une dans l'espace de nommage de x. Ces
## variables vont évoluer indépendemment.

spam.x = 5
x = 6
print spam.x
print x

## En résumé, nous avons deux manières d'importer des modules
## avec des propriétés très différentes. 
## L'instruction import permet d'importer un objet module. Avec
## cette importation, il y a une parfaire isolation des espaces
## de nommage puisque l'on ne peut accéder aux variables
## du module importé qu'à partir de son nom point la
## variable, par exemple spam.x. Par contre, on a un accès
## direct aux variables du module, il faut donc faire
## attention si on les modifies puisqu'elles seront
## modifiée dans l'espace de nommage du module. 

## L'autre manière d'importer un module est d'utiliser
## l'instruction from module import variable. Cette
## instruction va créer une nouvelle variable dans
## l'espace de nommage local qui référence le même objet 
## que la variable dans l'espace de nommage du module importé.
## L'avantage de cette importation est que l'on peut accéder
## directement à l'objet défini dans le module sans utiliser
## le nom du module point le nom de la variable. 
## C'est très utile pour les fonctions que l'on utilise
## très souvent. 

import math
math.cos(10)

from math import cos
cos(10)

## Par contre, comme la fonction est importé dans l'espace
## de nommage local, il faut faire attention aux collisions,
## c'est-à-dire que le nom de variable importé n'existe
## par déjà localement, sinon il sera remplacé par le
## nom de variable importé. 

