
# Héritage, typage

## Complément - niveau intermédiaire

Dans ce bref complément, nous allons tenter d'attirer votre attention sur une
différence assez essentielle entre python et les langages statiquement typés, et
qui peut avoir son importance quand il s'agit de concevoir une hiérarchie
d'héritage.

Je précise avant de commencer que contrairement à la grande majorité des
compléments, je décris  ici un **sentiment personnel** plutôt que des **faits
établis**, et je vous invite à le prendre comme tel.

### Type et type

Revenons sur la notion de type, et remarquons que les types peuvent jouer
plusieurs rôles, comme on l'a évoqué rapidement en première semaine&nbsp;:
 1. d'une part la notion de type a à voir avec l'implémentation, par exemple, un
compilateur C a besoin de savoir très précisément quel espace allouer à une
variable&nbsp;;
 1. d'autre part, les types sont cruciaux dans les systèmes de vérification
statique au sens large dont le but est de trouver un maximum de défauts à la
seule lecture du code (par opposition aux techniques qui nécessitent de le faire
tourner).

### On peut avoir tendance à les mélanger

Dans les langages typés statiquement, on utilise l'héritage dans ces deux
dimensions du typage.

##### Implémentation

Bien sûr l'héritage sert d'abord et avant tout à partager les implémentations,
et donc si la classe `A` hérite de la classe `B`, le compilateur va se
débrouiller pour faire ce qu'il faut pour que ce qui s'applique à `A` s'applique
à `B`.

##### Type-checking

La hiérarchie de classes est aussi un moyen privilégié de décrire les types de
la deuxième sorte. Si je prends l'exemple classique d'un système graphique, on
va avoir tendance - toujours avec un langage à la C++ ou Java - à&nbsp;:
 * se définir une hiérarchie de classes qui ressemble à ceci&nbsp;:

    Graphic
        |-- Circle
        |-- Square
        |-- Text
        |-- ...
 * définir `Graphic` comme une **classe abstraite**, qui **spécifie** que les
classes filles doivent implémenter, disons la méthode `void draw()`,
 * ce qui permet ensuite d'écrire quelque chose comme (xxx Valérie j'aurais
besoin que tu me traduises ça en vrai C++, sans forcément entrer dans les
détails xxx; j'ai juste besoin que le type Graphic apparaisse)

    void Display (Graphic* dessin) {
        for (graphic = dessin; graphic; graphic ++) {
            graphic->draw();
        }
    }


Dans cet exemple l'existence de `Graphic` permet de typer `Display`, et permet
au type-checker de s'assurer que tous les appels à `draw()` seront correctement
résolus à run-time.

### C'est différent en python

En python, ce n'est pas du tout comme cela qu'on a pris le problème.

Bien sûr on hérite de l'implémentation comme dans les autres langages.

Mais pour la deuxième dimension, le système de types de python est connu sous le
nom de [*duck typing*](http://en.wikipedia.org/wiki/Duck_typing), une
appellation qui fait référence à cette phrase

    When I see a bird that walks like a duck and swims like a duck and quacks
like a duck, I call that bird a duck.

Dans notre cas, cela signifie, si on considère un fragment qui fait
principalement la même chose que tout à l'heure&nbsp;:

    for graphic in dessin:
        graphic.draw()

et si on essayait de le typer statiquement, on en arriverait à la conclusion
qu'il faut&nbsp;:
 * que `dessin` soit itérable, et
 * que chacun de ses éléments possède l'attribut `draw`, qui soit un `callable`,
qu'on peut invoquer comme une méthode sans argument.


Ce qui signifie que je peux faire tourner *ce code-là* - et non pas un clone que
j'obtiendrais par exemple au moyen d'un système de template - sur un objet
`dessin` qui serait&nbsp;:
 * un tuple de graphiques,
 * une liste de graphiques,
 * une instance itérable de mon cru dont les éléments sont des graphiques,
 * ou une liste d'objets d'une classe qui n'a rien à voir sauf qu'elle a une
méthode `draw` aussi.

Même si la dernière famille est un peu tirée par les cheveux dans notre exemple,
pensez si vous préférez à la possibilité de faire une moyenne sur des objets;
tout ce qu'il vous faut c'est savoir additionner et diviser (plus là dessus dans
la prochaine séquence).

Dans tous les cas j'espère qu'à ce stade vous êtes convaincus qu'on ne **peut
pas** exprimer ces propriétés en termes simplement de relation d'héritage à la
`isinstance`.

Vous voyez donc que ce modèle de `duck typing` est d'une nature très différente
de ce qui se pratique dans les langages statiquemenet typés.

### `isinstance` sur stéroïdes

D'un autre côté, c'est très utile d'exposer au programmeur un moyen de vérifier
si un objet a un *type* donné - dans un sens volontairement vague ici.

On a déjà parlé - en Semaine 4, séquence "les fonctions" - de l'intérêt qu'il
peut y avoir à tester le type d'un argument avec `isinstance` dans une fonction,
pour parvenir à faire l'équivalent de la surcharge en C++ (la surcharge en C++
c'est quand vous définissez plusieurs fonctions qui ont le même nom mais des
types d'arguments différents).

C'est pourquoi quand on a cherché à exposer au programmeur des propriétés comme
"cet objet est-il iterable" on a choisi d'étendre *isinstance* au travers de
[cette initiative](http://legacy.python.org/dev/peps/pep-3119/). C'est ainsi
qu'on peut faire par exemple&nbsp;:


    from collections import Iterable


    isinstance('ab', Iterable)


    isinstance([1, 2], Iterable)


    # comme on l'a vu un objet qui a une methode  __iter__()
    # et une next() est considere comme un iterable
    class Foo():
        def __iter__(self):
            return self
        def next(self):
            # ceci naturellement est bidon
            return 
            
    foo = Foo()
    isinstance(foo, Iterable)

L'implémentation du module `abc` donne l'**illusion** que `Iterable` est un
objet dans la hiérarchie de classe, et que tous ces *types* `str`, `list`, et
`Foo` lui sont asujettis, mais ce n'est pas le cas en réalité; ces trois types
ne sont pas comparables dans la hiérarchie de classes, ils n'ont pas de plus
petit (ou plus grand) élément.

Je signale pour finir sur `isinstance` et le module `collections` que la
définition du symbole `Hashable` est à mon avis beaucoup moins convaincante que
`Iterable`; si vous vous souvenez qu'en Semaine 3, Séquence "les dictionnaires",
on avait vu que les clés doivent être globalement immuables. C'est une
caractéristique qui est assez difficile à écrire, et en tous cas ceci de mon
point de vue ne remplit pas la fonction&nbsp;:


    from collections import Hashable


    # un tuple qui contient une liste ne convient 
    # pas comme clé dans un dictionnaire
    # et pourtant
    isinstance (([1], [2]), Hashable)

### Tout ça pour dire quoi ?

Au-delà de cette opinion, les points à retenir de ce complément un peu digressif
sont&nbsp;:
 * en python, on hérite des **implémentations** et pas des **spécifications**;
 * et le langage n'est pas taillé pour tirer profit de **classes abstraites** -
même si rien ne vous interdit d'écrire, pour des raisons documentaires, une
classe qui résume l'interface qui est attendue par tel ou tel système de plugin;


Venant de C++ ou de Java, cela peut prendre du temps d'arriver à se débarrasser
de l'espèce de réflexe qui fait qu'on pense d'abord classe abstraite, puis
implémentations.
