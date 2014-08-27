# -*- coding: iso-8859-15 -*-

## Je vais créer une variable globale et une fonction
L = 10

def f():
    L = 11

print L
f()
print L

## La variable locale L ne modifie par la variable globale L
## Par contre, si l'on rajoute l'instruction global, alors
## ça veut dire que la variable L assignée dans la fonction
## est bien la variable globale. L'instruction global permet
## de changer le scope d'une variable assignée localement
## dans une fonction. 

def f():
    global L
    L = 11

print L
f()
print L

## globale est une intruction un peu particulière en Python
## Ça n'est pas une instruction interprété comme toutes les
## autres instruction, c'est une directive au compilateur
## qui génère le byte code avant l'exécution. Donc, une
## variable définie comme étant globale le sera pour tout le
## scope dans lequel l'instruction global est présente,
## quelque soit la position de global dans ce scope.

def f():
    L = 12
    global L
f()
print L

## L est globale pour toute la fonction h(), même si globale
## est définie après l'assignation 'L = 12'. Attention,
## dans les nouvelles version de Python, il sera interdit
## de mettre la directive global après la variable que l'on
## veut rendre global. Il faut donc prendre l'habitude
## de mettre global au tout début des fonctions. 

# 2 minutes 30

## Pour finir, la directive global doit être utilisée avec
## parcimonie. En effet, modifier une variable global
## dans une fonction en utilisant la directive globale
## rend le code difficile à suivre. Il faut toujours
## privilégier les moficication explicite par retour
## de fonction. Regardon ces deux exemples

x = 100
def f():
    global x
    x = x + 10
f()
print x

## Regardons maintenant une autre manière d'écrire
## le même code

x = 100
def f():
    return x + 10
x = f()
print x

## dans le premier cas la modification de x est implicite,
## mais dans le deuxième cas  c'est explicique avec
## l'assignation du resultat de f() à la variable x. Il faut
## toujours privilégier ce deuxième cas. 

## 4 minutes. 
