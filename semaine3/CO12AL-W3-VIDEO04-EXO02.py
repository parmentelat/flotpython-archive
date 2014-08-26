# -*- coding: iso-8859-15 -*-

## Prenons une liste de 3 éléments

liste = [1, 2, 3]

## essayons d'appeler next() sur la liste L
#liste.next()

## ça retourne une exception parce que la list L
## n'est pas un itérateur. Par contre les listes ont
## des itérateurs.

## recupérons l'itérateur de cette liste

iterateur = liste.__iter__()

## nous voyons que la liste et l'itérateur sont différents
print liste is iterateur

## par contre si on appelle __iter__() sur l'itérateur
## on remarque de l'on a le même objet, donc
## l'appelle de __iter__() sur un itérateur retourne bien
## l'itérateur lui même.

iterateur2 = iterateur.__iter__()

print iterateur is iterateur2

## on peut faire directement une boucle for sur l'itérateur
## c'est équivallent à faire une boucle for sur l'objet
## qui a cet itérateur puisque la boucle for appélera toujours
## en premier la fonction __iter__() sur l'objet.

for element in iterateur:
    print element,

## par contre, une fois que l'itérateur a retourné tous les
## éléments, next() retournera toujours StopIteration, on ne
## peut donc plus faire de boucle for dessus. Il faudra dans
## ce cas créer un autre itérateur.

#iterateur.next()

for element in iterateur:
    print element, 

iterateur3 = liste.__iter__() # nouvel itérateur

print
print iterateur is iterateur3

for element in iterateur3:
    print element,
    
## Il faut faire attention lorsque l'on manipule directement des itérateurs
## de générer un nouvel itérateur à chaque fois que l'on fait une nouvelle
## boucle. On n'a pas de ce problème avec les objets qui ont des itérateurs
## puisque la boucle for se chargera elle même de génerer un nouvelle itérateur
    
