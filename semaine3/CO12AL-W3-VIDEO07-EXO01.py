# -*- coding: iso-8859-15 -*-

## La syntaxe d'une fonction lambda est simple.
## Elle commence par le mot clef lambda, suivi
## d'une liste d'argument séparé par des virgules
## et d'un expression pouvant utiliser ses arguments.

lambda x: x**2 + 2*x -1

## Cependant les fonctions lambda n'ont pas de nom
## alors comment les utiliser ? Le résultat
## de l'évaluation du code de la fonction lambda est une
## référence vers l'objet fonction qui vient d'être créé

## On peut donc utiliser une fonction lambda de deux
## manieres, soit on lui donne un nom en l'assignant à
## une variable, soit on la définie directement là où
## elle va être utilisée. 

f = lambda x: x**2 + 2*x - 1

print f(1)

L = [lambda x: x**2 + 2*x - 1, lambda x: x**3 -2]

print L[0](10), L[1](10)

## on peut également directement passer une fonction
## lambda à une fonction

def func(x):
    for i in range(10):
        print i, x(i)

## Je suppose lors de l'écriture de ma fonction func
## que l'argument x sera une fonction. Si x n'est pas
## une fonction j'aurai une exception

# func(1)

func(lambda x: x**2 -3)

## il est très important de comprendre que je peux
## faire exactement la même chose avec une fonction
## classique. Après tout en Python, tout est un objet
## et une variable n'est qu'un nom qui référence un
## objet, en particulier, le nom d'un fonction
## référence l'objet fonction défini par le def.

def g(x):
    return x**2 -3
func(g)

## la fonction lambda permet simplement d'écrire
## plus rapidement les fonctions qui sont limitée
## à une seule expression. En effet, dans une fonction
## lambda, on ne peut pas mettre d'instructions comme
## des if ou des for. 

# 4 minutes

## Un usage classique des fonctions lambda en Python est
## de les utiliser avec les fonctions built-in map() et
## filter().

## Je vous rappelle qu'en Python les itérateurs sont au coeur
## de la programmation et qu'avec les boucles for,
## on peut de manière simple et efficace exploiter la
## puissance des itérateurs. Il existe cependant d'autres
## moyen d'exploiter les itérateurs en Python

