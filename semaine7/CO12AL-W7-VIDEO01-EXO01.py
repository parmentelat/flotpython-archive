# -*- coding: iso-8859-15 -*-

## Supposons que l'on veuille compter le nombre d'instances
## créées par une classe. On peut facilement maintenir un
## compteur du nombre de référence dans contructeur de la
## classe, mais l'accès à ce compteur n'est pas trivial.
## Regardons cela...


class C:
    nb_i = 0
    def __init__(self):
        C.nb_i  = C.nb_i + 1


C()
C()
## je peux évidamment accéder à l'attribut de la
## classe directement. 
print C.nb_i

## Je peux aussi faire une fonction dans mon module

def f():
    return C.nb_i


print f()

## Mais cela complique la maintenance d'avoir une fonction
## travaillant sur une classe en dehors de la classe.
## Par contre, je ne peux pas faire une méthode d'instance
## dans ma classe puisqu'il me faut une instance pour accéder
## au compteur, et que cette instance va changer le compteur
## à sa création.

## La solution ici est d'avoir une méthode statique.
## une méthode statique s'écrit comme une fonction,
## mais doit être déclarée comme statique avec la
## fonction staticmethod. 

class C:
    nb_i = 0
    def __init__(self):
        C.nb_i  = C.nb_i + 1
    def f():
        return C.nb_i
    f = staticmethod(f)

C()
C()
print C.f()

## notons qu'une méthode statique peut aussi être appelée sur
## une instance, mais que l'instance n'est pas passée à la
## méthode

print C().f()
