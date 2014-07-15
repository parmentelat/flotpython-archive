# -*- coding: latin_1 -*-

## l'instruction print afficher simplement la valeur d'un objet sur le terminal
## on dit également que l'on affiche une valeur sur la sortie standard

## print peut aussi bien accepter une variable (et dans ce cas il affiche
## la valeur de l'objet référencé par la variable) ou directement un objet.
## regardons cela en pratique

s = 'spam'
print s
print 'spam'

## l'instruction print permet aussi d'afficher plusieurs objets ou variable
## en les séparant par une virgule

i = 10

print i, s

## lorsqu'il y a une virgule entre les arguments (variable ou objet) passé
## à print, print ajoute un espace entre les valeurs des arguments retournés

## print ajoute automatiquement un retour chariot (c'est-à-dire, un saut de ligne)
## après la dernière valeur affichée. On peut supprimer ce saut de ligne en ajoutant
## une virgule après le dernier argument passé à print.

print s
print s

print s,
print s


## lorsque l'on est dans le terminal interactif, on peut aussi directement
## taper le nom de la variable suivi d'un retour chariot.

i

## On voit ainsi la représentation interne de l'objet ?
## c'est souvent équivallent à print (mais pas toujours).
## La représentation interne peut donner des informations
## supplémentaires.

