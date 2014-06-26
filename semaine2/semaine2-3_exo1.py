# -*- coding: cp1252 -*-

## opérations communes à toutes les séquences
## on prend comme example une chaîne de caractère
## où chaque caractère est un élément de la séquence

s1 = 'spam'
s2 = 'eggs'

## test d'appartenance

's' in s1
'x' in s1

'x' not in s1

## concaténation (retourne une nouvelle séquence)
## les deux séquences doivent être de même type

s1 + s2

## autres opérations
len(s1)
min(s1)
max(s1)

## indice de la première occurence de 'g'
s2.index('g')

## nombre d'occurence de 'g' dans la séquence
s2.count('g')

s1*3
'*'*20


s1[2]


## list
L = [1, 2.3, 'spam', False, 2354555L]
print L

## tuple
#Pour un tuple on remplace les crochés par des parenthèses
T = (1, 2.3, 'spam', False, 2354555L)
print T
