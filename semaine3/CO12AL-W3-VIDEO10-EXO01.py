# -*- coding: iso-8859-15 -*-

## Commençons pas sauvegarder notre éditeur dans un fichier
## finissant en .py, par exemple scope.py.
## Lorsque nous allons exécuter ce fichier
## (je vous rappelle que dans IDLE
## on peut simplement taper sur la touche F5, ou on
## peut en ligne de commande taper python scope.py)
## l'interpréteur Python va transformer le code dans ce
## fichier en un objet module. 
## Toutes les variables définies dans
## ce fichier appartiennent au scope global de ce module
## sauf les variables définies dans les fonctions.

## Il y a deux notions importantes à comprendre lorsque
## l'on parle de variables. La première notion est celle
## de scope qui explique comment les variables peuvent
## accéder aux différentes parties du code d'un même module.
## c'est ce que l'on va voir dans cette vidéo. La deuxième
## notion est celle d'espace de nommage qui explique
## comment accéder aux variables d'autres modules et d'autres
## objets. C'est ce que l'on verra lorsque l'on parlera
## des modules un peu plus tard. En résumé, le scope
## concerne l'accès aux variables internes au module,
## et les espaces de nommage concernent l'accès
## aux variables entre les modules.

## créeons deux variables a et b
a, b = 1, 1

## c'est une variable globale parce que définie dans un module
## et en dehors d'une fonction. Toutes les variables globales
## sont accéssibles à tout le code d'un module.

for i in range(10):
    print a


## je définis maintenant une fonction f avec deux variables
## b et c. Comme elles sont définies dans la fonction,
## elle sont locales, c'est-à-dire créées uniquement à
## l'appelle de la fonction et détruite lorsque la fonction
## retourne (c'est-à-dire lorsque l'on sort de la fonction)

def f():
    b, c = 2, 3
    print a, b, c

## lorsque je fais 'print a, b, c', comment l'interpréteur
## sait quelle variable 'a' utiliser. C'est très simple !
## la règle est de chercher d'abord la variable localement où
## elle est utilisée. Ici, c'est dans une fonction, donc
## on cherche 'a' localement dans la fonction,
## puis, si 'a' n'est pas trouvé dans le scope de la fonction,
## on cherche 'a' globalement, c'est-à-dire dans le module.
## Ici, a et b sont trouvées localement c'est eux
## que l'on utilise. 

f()

## 'print a' cherche 'a' localement où elle est utilisée,
## c'est-à-dire dans le scope global du module. 
print b

## par contre, on ne peut pas faire print 'c', puisque
## 'c' est une variable locale à la fonction, donc pas accéssible
## en dehors de la fonction. De plus, les variables locales
## des fonctions sont créées à chaque appel de la fonction
## et détruite lorsque la fonction retourne. 

#print c

## Les variables définies dans l'entête de la fonction sont
## également des variables locales

def f2(a):
    print a

f2(8)

print a

## mais gardons en tête qu'utiliser localement dans une
## fonction un nom global est toujours une mauvaise idée.
## En Python on doit utiliser des noms de variables explicites
## et nous verrons prochainement qu'utiliser localement
## un nom de variable globale peut conduire à des erreurs
## surprenantes.

## Maintenant, que ce passe-t-il si on définit une fonction
## dans une fonction.

a, b, c = 1, 1, 1
def g():
    b, c  = 3, 4
    def h():
        c = 5
        print a, b, c
    h()
g()

## Python va suivre dans ce cas une nouvelle règle. Lorsque
## l'on fait 'print a, b, c' dans la fonction h(),
## Python cherche les variables dans le scope local de h(),
## il trouve 'c' qui vaut 5, puis, et c'est la nouvelle règle,
## dans tous les scopes des fonctions englobante, c'est-à-dire
## des fonctions qui contiennent le bloc de code de h(),
## de la fonction la plus proche de h,
## jusqu'à la plus éloignée. Python trouve 'b' qui vaut 3, 
## puis Python cherche dans le scope global et trouve 'a' qui
## vaut 1.

## résumons, le scope d'une variable est déterminé par le bloc
## de code dans lequel est défini la variable. Il peut être
## local (dans une fonction) ou global (dans le module).
## Ensuite on cherche la définition d'une variable localement,
## puis dans le scope des fonctions englobantes, puis
## globalement. On appelle cette règle LEG.
