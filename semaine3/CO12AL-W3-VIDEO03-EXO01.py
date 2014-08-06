# -*- coding: iso-8859-15 -*-

## il y a trois opérateurs de tests booléens en Python
## and, or et not. A and B est vrai si A et B sont vrais,
## A or B est vrai A ou B est vrai, not A est vrai si A
## est faux.Regardons quelques exemples. 
print 1 < 2 and 3 < 4

print 1 < 2 or 3 > 4

print not 1 < 2

## On remarque qu'encore une fois la syntaxe est proche
## du langage naturel

## Les opérateurs and et or sont shortcircuits, c'est-à-dire
## que l'argument de droite n'est pas toujours évalué.
## Si on fait A and B, B n'est évalué que si A est vrai
## Si on fait A ou B, B n'est évalué que si A est faux.
## Regardons un exemple :
## la fonction func() n'est pas définie

#func()

print 3 < 2 and func()

print 1 < 2 or func()

## pour finir on peut combiner les opérateurs, chaque
## opérateur ayant un priorité spécifique. Je ne vous
## expliquerai pas ces règles, parce qu'il vaut mieux
## les rendre explicites en utilisant des paranthèses

print (1 < 2 and (not 3 > 4)) or 1 == 1
