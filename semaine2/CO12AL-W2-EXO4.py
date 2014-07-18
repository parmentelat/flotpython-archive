# -*- coding: latin_1 -*-

## une liste est une séquence, donc toutes les fonctions et opérations
## que l'on a vues pour les séquences s'appliques aux listes : en particulier
## testes d'appartenance in, not in ; concaténation avec le signe + ;
## longeur avec la fonction built-in len ; récupération d'un élément
## par son index entre crochet ; et le slicing.

## on crée une liste vide ainsi
l = []

## on sépare les éléments d'une liste par des virgules
## notons que l'on peut directement mettre un objet dans
## la liste, ou utiliser une variable référencant l'objet

i = 4

l = [i, 'spam', 3.2, True]

print l[0]

l[0] = 20

print l

## on peut également directement effectuer une opération et réaffecter
## cette opération à un élément de la liste. Je rappelle qu'en Python
## on évalue d'abord ce qu'il y a à droite du signe égal et ensuite
## on affecte le résultat à la variable de gauche.

l[0] = l[0] + 1

print l

## on peut utiliser le slicing dans une liste parce que c'est
## une séquence

print l[1:2]

## mais comme une liste est mutable on peut affecter sur slice

l[1:2] = ['egg', 'beans']

print l

## il faut bien comprendre ce que fait cette opération. Python commence
## par effacer les éléments spécifiés par le slide dans l, puis il va
## ajouter les éléments de la liste de droite à la place. S'il y a plus
## d'éléments la liste est agrandie, s'il y en a moins, elle est raccoucie

## on peut donc supprimer des éléments sur un slice en affectant un slice à une
## liste vide

l[1:2] = []

print l

## je peux également utiliser l'instruction del pour effacer tous les éléments
## spécifiés dans un slice

del l[0:3:2]

print l

## par contre s'il on écrit L[1] = ['spam', 'good'], on va simplement ajouter
## une liste à la position 1 de la liste l

l[1] = ['spam', 'good']

print l

## avant de continuer, sur les fonctions spécifiques aux listes, je vais
## introduire la fonction built-in range() qui permet d'obtenir une liste
## d'entiers.

print range(10)

print range(1, 10)

print range(1, 10, 2)

## Regardons maintenant les 7 fonctions qui permettent de modifier
## les listes en place.

l = range(10)

l.append('spam')
print l

l.extend([11, 12])
print l

## insert l'objet juste avant la position, mais n'efface et ne remplace rien
l.insert(2, 'egg')
print l

l.sort() # attention sort ne retourne pas la liste, mais la modifie en place
print l

l.reverse()
print l

print l.pop()

print l.pop(2)

print l

l.remove(5) # efface la premiere occurence de l'élément passé en parametre

## 8 minutes
