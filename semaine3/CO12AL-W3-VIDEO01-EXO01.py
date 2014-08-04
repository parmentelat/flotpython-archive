# -*- coding: iso-8859-15 -*-

## Pour charger un module il faut utiliser l'instruction
## import

import math

## ensuite, pour utiliser le module, on utilise le même nom
## que celui que l'on a utilisé pour l'import. On peut
## voit tous les attributs d'un module avec l'instruction
## dir

print dir(math)

## un attribut est une variable reférencant un objet.
## Comme en Python tout est un objet, un attribut peut être
## n'importe quoi en Python : un type de base, une fonction,
## un module, ou d'autres objets que l'on verra dans
## les semaines qui viennent comme les classes.

## Pour accéder à l'attribut d'un objet, on utilise
## le nom de l'objet point le nom de l'attribut. 

print math.log(10)

## Pour connaître à quoi correspond un attribut on peut
## utiliser la fonction built-in help()

help(math.log)

## on peut aussi appeler help() directement sur un module
## mais il a y en général trop de texte et il est plus
## pratique de regarder directement l'aide fournie avec
## Python ou sur le Web.

help(math)

## et on peut bien sur combiner des attributs de modules
print math.tan(math.pi/4)


