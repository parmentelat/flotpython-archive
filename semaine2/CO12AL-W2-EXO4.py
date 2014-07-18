# -*- coding: latin_1 -*-

## une liste est une séquence, donc toutes les fonctions et opérations
## que l'on a vues pour les séquences s'appliques aux listes : en particulier
## testes d'appartenance in, not in ; concaténation avec le signe + ;
## longeur avec la fonction built-in len ; récupération d'un élément
## par son index entre crochet ; et le slicing.

## on crée une liste vide ainsi
L = []

## on sépare les éléments d'une liste par des virgules

L = [4, 'spam', 3.2, True]

## notons que l'on peut directement mettre un objet dans
## la liste, ou utiliser une variable référencant l'objet

print L[1]

L[0] = L[0] + 1

print L
