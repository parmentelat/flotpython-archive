
# Surcharge d'opérateurs (1)

## Complément - niveau intermédiaire

Ce complément vise à illustrer certaines des possibilités de surcharge
d'opérateurs. Comme annoncé dans la vidéo, il existe un total de près de 80
méthodes dans ce système de surcharges, aussi il n'est pas question ici d'être
exhaustif. Vous trouverez [dans ce document une liste complète de ces
possibilités](http://docs.python.org/2/reference/datamodel.html#special-method-
names).

Il nous faut également signaler que les mécanismes mis en jeu ici sont de
difficultés assez variables. Dans le cas le plus simple il suffit de définir une
méthode sur la classe pour obtenir le résultat (par exemple, définir `__call__`
pour rendre un objet callable). Mais parfois on parle d'un ensemble de

Pour alléger la présentation, cet exposé a été coupé en deux notebooks
différents, de manière arbitraire.

*****

### Rappels (1)

Pour rappel, on a vu dans la vidéo&nbsp;:
 * la méthode `__init__` pour définir un **constructeur**,
 * et la méthode `__str__` pour définir comment une instance s'imprime avec
`print`.

### Affichage : `__repr__` et `__str__`

Nous commençons par signaler la méthode `__repr__` qui est assez voisine de
`__str__`, et qui donc doit retourner un objet de type chaîne de caractères,
sauf que&nbsp;:
 * `__str__` est utilisé par `print` (affichage orienté utilisateur du
programme; priorité au confort visuel),
 * alors que `__repr__` est utilisée par la fonction `repr()` (affichage orienté
programmeur, aussi peu ambigü que possible);
 * il faut savoir que `__repr__` est utilisé **aussi** par `print` si `__str__`
n'est pas défini.

Pour cette seconde raison, on trouve dans la nature `__repr__` plutôt plus
souvent que `__str__`; voyez [ce
lien](https://docs.python.org/2/reference/datamodel.html#object.__repr__) pour
davantage de détails.

##### Quand est utilisée `repr()`

`repr()` est utilisée massivement dans les informations de debugging comme les
traces de pile lorsqu'une exception est levée. Elle est aussi utilisée lorsque
vous affichez un objet sans passer par `print`, c'est-à-dire par exemple&nbsp;:


    class Foo: pass
    foo = Foo()
    # lorsque vous affichez un objet comme ceci
    foo
    # en fait vous utilisez repr()




    <__main__.Foo instance at 0x1102dbd88>



##### Deux exemples

Voici deux exemples simples de classes; dans le premier on on n'a défini que
`__repr__`, dans le second on a redéfini les deux méthodes&nbsp;:


    # une classe qui ne définit que __repr__
    class Point (object):
        "première version de Point - on ne définit que __repr__"
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return "Point({x},{y})".format(**vars(self))
        
    point = Point (0,100)
    
    print "avec print", point
    
    # si vous affichez un objet sans passer par print
    # vous utilisez repr()
    point


    avec print Point(0,100)





    Point(0,100)




    # la même chose mais où on redéfinit __str__ et __repr__
    class Point2 (object):
        "seconde version de Point - on définit __repr__ et __str__"
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return "Point2({x},{y})".format(**vars(self))
        def __str__(self):
            return "({x},{y})".format(**vars(self))
        
    point2 = Point2 (0,100)
    
    print "avec print", point2
    
    # format utilise aussi __str__
    print "avec format {}".format(point2)
    
    # si vous affichez un objet sans passer par print
    # vous utilisez repr()
    point2

    avec print (0,100)
    avec format (0,100)





    Point2(0,100)



*****

### Rappels (2) : `__iter__`

Nous avons vu en semaine 3, dernière séquence "Les boucles `for` et les
itérateurs", qu'un objet peut être utilisé par le langage comme un
***itérable*** s'il possède une méthode `__iter__` qui renvoie un itérateur. On
rappelle qu'un itérable peut notamment être l'objet d'une boucle `for`, mais
aussi dans les fonctions comme `zip` ou `map`.

### `__call__`

Le langage introduit également la notion de ***callable*** - littéralement, qui
peut être appelé.
L'idée est très simple, on cherche à donner un sens à un fragment de code du
genre de&nbsp;:

                # on crée une instance
objet = Classe (arguments)
# et on l'utilise comme une fonction
objet (arg1, arg2)
                
Le protocole ici est très simple; cette dernière ligne a un sens en python dès
lors que&nbsp;:
 * `objet` possède une méthode `__call__`,
 * et que celle-ci peut être appelée sur `objet` avec les arguments `arg1,
arg2`, pour nous donner le résultat associé à `objet (arg1, arg2)`.

Voyons cela sur un exemple&nbsp;:


    class PlusClosure (object):
        """Une classe callable qui permet de faire un peu comme la 
        fonction built-in sum mais avec en ajoutant une valeur initiale"""
        def __init__ (self, initial):
            self.initial = initial
        def __call__ (self, *args):
            return self.initial+sum(args)
        
    # on crée une instance avec une valeur initiale 2 pour la somme
    plus2 = PlusClosure (2)
    
    # on peut maintenant utiliser cet objet 
    # comme une fonction qui fait sum(*arg)+2
    
    print '[] ->', plus2()
    
    print '1 ->', plus2(1)
    
    print '1,2 ->', plus2(1,2)

    [] -> 2
    1 -> 3
    1,2 -> 5


Pour ceux qui connaissent, nous avons choisi à dessein un exemple qui
s'apparente à [une
clôture](http://en.wikipedia.org/wiki/Closure_%28computer_programming%29). Nous
reviendrons sur cette notion de *callable* lorsque nous verrons les décorateurs
en semaine 7.

### `__getattr__` et apparentés

### `__nonzero__`

### `__contains__`

### opérations arithmétiques

### `__getitem__` et apparentés


    
