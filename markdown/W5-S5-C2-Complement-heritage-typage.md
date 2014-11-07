
# Héritage, typage

## Complément - niveau intermédiaire

Dans ce complément nous allons tenter d'attirer votre attention sur une
différence assez essentielle entre python et les langages statiquement typés,
quand il s'agit de concevoir une hiérarchie d'héritage.

### Rappels sur les types

Un système de types est ce qui permet au langage de décider, plus ou moins à
l'avance, si telle ou telle instruction ou fragment de code a un sens avant
d'essayer de l'exécuter.

On l'a mentionné rapidement au cours des semaines précédentes, mais les langages
typés statiquement ont pour l'essentiel un système de types basés sur les
classes. Pour faire simple un objet est d'un type `Foo` si et seulement si sa
classe est une sous-classe de Foo.

En python, ce n'est pas du tout comme cela qu'on a pris le problème. Le système
de type de python est connu sous le nom de [*duck
typing*](http://en.wikipedia.org/wiki/Duck_typing), une appellation qui fait
référence à cette phrase

    When I see a bird that walks like a duck and swims like a duck and quacks
like a duck, I call that bird a duck.

Dans notre cas, cela signifie si on considère un fragment comme ceci&nbsp;:

    for graphic in vector:
        graphic.redraw()

et si on essayait de le typer statiquement, on en arriverait à la conclusion
qu'il faut&nbsp;:
 * que `vector` soit itérable, et
 * que chacun de ses éléments possède l'attribut `redraw`, qui soit un
`callable`.

J'espère qu'à ce stade vous êtes convaincus qu'on ne **peut pas** exprimer ces
propriétés en termes simplement de relation d'héritage à la `isinstance` -
quoique [cette initiative]() vise précisément à permettre de tester des
propriétés comme *"l'objet x est-il itérable ?"* au moyen d'un `isinstance` sur
stéroides.

### À quoi l'héritage **ne sert pas** en python

Dans le cas d'un langage typé statiquement comme C++ ou Java, on a tendance par
contre, pour satisfaire le compilateur, à **définir une classe abstraite**, dans
notre cas `Graphic`, qui **spécifie** que les sous-classes doivent implémenter
la méthode `redraw`. Et donc à concevoir une hiérarchie comme

    Graphic
    |-- Circle
    |-- Square
    |-- Text
    |-- ...

En python, **rien ne nous oblige** à déclarer une classe **uniquement** pour
matérialiser le fait qu'un objet dispose de la méthode `redraw()`. Sans aller
jusqu'à dire que cette classe est néfaste, la valeur ajoutée d'en définir une
n'est pas immédiatement établie.

Par contre si on parle **d'implémenter** quelque chose comme `GraphicContext`
(des couleurs, des fontes, ..) l'intérêt est parfaitement évident; à mon avis
toutefois on parle de quelque chose de différent de `Graphic`.

Au-delà de cette opinion, les points à retenir de ce complément un peu digressif
sont&nbsp;:
 * en python, on hérite des **implémentations** et pas des **spécifications**;
il arrive parfois que pour des raisons documentaires on écrive des classes qui
résument l'interface qui est attendue par tel ou tel système de plugin, mais le
langage n'est pas taillé pour cela;
 * c'est pourquoi, avant de créer une classe, il peut être utile de se demander
si il y a une réelle valeur ajoutée en termes d'implémentation à partager.
