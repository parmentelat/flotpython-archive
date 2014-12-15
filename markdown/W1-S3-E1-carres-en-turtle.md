
# Dessiner un carré

## Exercice - niveau intermédiaire

Voici un tout petit programme qui dessine un carré

Il utilise le module `turtle`, conçu précisément à des fins pédagogiques. Pour
des raisons techniques, le module `turtle` n'est **pas disponible** au travers
de la plateforme FUN.

Il est donc inutile d'essayer d'exécuter ce programme depuis le notebook;
l'objectif de cet exercice est plutôt de vous entraîner à télécharger ce
programme en utilisant le menu *"File -> Download as -> python"*, puis à le
charger dans votre IDLE pour l'exécuter sur votre machine.


    # we need the turtle module
    import turtle

On commence par définir une fonction qui dessine un carré de coté `length`


    def square(length):
        "have the turtle draw a square of side <length>"
        for side in range(4):
            turtle.forward(length)
            turtle.left(90)

Maintenant on commence par initialiser la tortue


    turtle.reset()

On peut alors dessiner notre carré


    square(200)

Et pour finir on attend que l'utilisateur clique dans la fenêtre de la tortue,
et alors on termine


    turtle.exitonclick()

## Exercice - niveau avancé

Naturellement vous pouvez vous amuser à modifier ce code pour dessiner des
choses un peu plus amusantes.

Dans ce cas, commencez par chercher "module python turtle" dans votre moteur de
recherche favori, pour localiser la documentation du module
[`turtle`](https://docs.python.org/2/library/turtle.html).

Vous trouverez quelques exemples pour commencer ici:
 * [turtle_multi_squares.py](media/turtle_multi_squares.py) pour dessiner des
carrés à l'emplacement de la souris en utilisant plusieurs tortues;
 * [turtle_fractal.py](media/turtle_fractal.py) pour dessiner une fractale
simple;
 * [turtle_fractal_reglable.py](media/turtle_fractal_reglable.py) une variation
sur la fractale, plus parametrable.

