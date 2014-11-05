
# Surcharge d'opérateurs (1)

## Complément - niveau intermédiaire

Ce complément vise à illustrer certaines des possibilités de surcharge
d'opérateurs. Comme annoncé dans la vidéo, il existe un total de près de 80
méthodes dans ce système de surcharges, aussi il n'est pas question ici d'être
exhaustif. Vous trouverez [dans ce document une liste complète de ces
possibilités](http://docs.python.org/2/reference/datamodel.html#special-method-
names).

Il nous faut également signaler que les mécanismes mis en jeu ici sont **de
difficultés assez variables**. Dans le cas le plus simple il suffit de définir
une méthode sur la classe pour obtenir le résultat (par exemple, définir
`__call__` pour rendre un objet callable). Mais parfois on parle d'un ensemble
de méthodes qui doivent être cohérentes, voyez par exemple les
[descriptors](https://docs.python.org/2/reference/datamodel.html#invoking-
descriptors) qui mettent en jeu les méthodes `__get__`, `__set__` et
`__delete__`, et qui sont particulièrement cryptiques.

Nous vous conseillons de commencer par des choses simples, et surtout de
n'utiliser ces techniques que lorsqu'elles apportent vraiment quelque chose. Le
constructeur et l'affichage sont pratiquement toujours définis, mais pour tout
le reste il convient d'utiliser ces traits avec le plus grand discernement. Dans
tous les cas écrivez votre code avec la documentation sous les yeux, c'est plus
prudent :)

Nous avons essayé de présenter cette sélection par difficulté croissante.
Par ailleurs, et pour alléger la présentation, cet exposé a été coupé en deux
notebooks différents.

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

*****

### `__nonzero__`

Vous vous souvenez que la condition d'un test dans un `if` peut ne pas retourner
un booléen (nous avons vu cela en Semaine 2, Séquence "Introduction aux tests
if/else"). Nous avions noté que pour les types prédéfinis, sont considérés comme
*faux* `None`, la liste vide, un tuple vide, etc...

Avec `__nonzero__` on peut redéfinir le comportement des objets d'une classe
vis-à-vis des conditions.

**Attention** pour éviter les comportements imprévus, comme on est en train de
redéfinir le comportement des conditions, il **faut** renvoyer un **booléen**
(ou à la rigueur 0 ou 1), on ne peut pas dans ce contexte retourner d'autres
types d'objet.

Nous allons illustrer cette méthode dans un petit moment.

### `__mul__` et apparentés (`__add__`, `__sub__`, `__div__`, `__and__`, etc..)

On peut également redéfinir les opérateurs arithmétiques et logiques. Dans
l'exemple qui suit nous allons l'illustrer sur la multiplication de matrices.
Pour mémoire&nbsp;:

$ \left( \begin{array}{cc} a_{11} & a_{12} \\
a_{21} & a_{22}\end{array} \right)
\times
\left( \begin{array}{cc} b_{11} & b_{12} \\
b_{21} & b_{22}\end{array} \right)
=
\left( \begin{array}{cc} a_{11}b_{11}+a_{12}b_{21} & a_{11}b_{12}+a_{12}b_{22}
\\
a_{21}b_{11}+a_{22}b_{21} & a_{21}b_{12}+a_{22}b_{22}\end{array} \right) $

Voici un exemple sur notre classe de matrices 2x2. Bien que ce ne soit pas le
sujet, cette implémentation illustre aussi la possibilité de construire la
matrice à partir&nbsp;:
 * soit des 4 coefficients
 * soit d'une séquence des 4 coeffcients


    # notre classe Matrix2 avec encore une autre implémentation
    class Matrix2 (object):
        def __init__(self, *args):
            # on veut pouvoir créer l'objet à partir des 4 coefficients
            if len(args) == 4:
                self.coefs = tuple(args)
            # ou bien d'une séquence de 4 coefficients
            elif len(args) == 1:
                self.coefs = tuple(*args)
        def __repr__(self):
            return "[" + ", ".join(["{}".format(c) for c in self.coefs]) + "]"
        def __mul__(self, m1):
            self.coefs[0],self.coefs[1],self.coefs[2],self.coefs[3] = \
                self.coefs[0]*m.coefs[]
                xxx
        def __nonzero__(self):
            # on considère que la matrice est non nulle 
            # si un au moins de ses coefficients est non nul
            # ATTENTION le retour doit être un booléen ou à la rigueur 0 ou 1
            # cette version-ci n'est pas correcte !
            # return [coef for coef in self.coefs if coef != 0.]
            return len([coef for coef in self.coefs if coef != 0.])!=0

On peut à présent créer deux objets et vérifier que la matrice nulle se comporte
bien comme attendu&nbsp;:


    matrice = Matrix2 (1,2,3,4)
    zero    = Matrix2 ([0,0,0,0])
    
    if matrice: 
        print matrice,"n'est pas nulle"
    if not zero: 
        print zero,"est nul"


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

Pour ceux qui connaissent, nous avons choisi à dessein un exemple qui
s'apparente à [une
clôture](http://en.wikipedia.org/wiki/Closure_%28computer_programming%29). Nous
reviendrons sur cette notion de *callable* lorsque nous verrons les décorateurs
en semaine 7.

***

### `__contains__`


    class DualQueue (object):
        """Une double file d'attente FIFO"""
        def __init__(self):
            self.inputs = []
            self.outputs = []
        def __repr__ (self):
            return "<DualQueue, inputs={inputs}, outputs={outputs}>".format(**vars(self))
        def add_input(self, item):
            self.inputs.insert(0,item)
        def emit_output (self):
            return self.outputs.pop()
        def move_input_to_output (self):
            self.outputs.insert(0,self.inputs.pop())
        def __contains__(self, item):
            # __contains__ doit retourner un booléen qui indique
            # si item est dans la queue
            return item in self.inputs or item in self.outputs


    q = DualQueue ()
    q.add_input ('foo')
    q.move_input_to_output()
    q.add_input ('bar')
    print q
    print "foo appartient-il ?", 'foo' in q
    print "None appartient-il ?", None in q

### `__getitem__` et apparentés

### `__getattr__` et apparentés

### opérations arithmétiques
