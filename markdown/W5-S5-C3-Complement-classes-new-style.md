
# Classes "new style"

## Complément - niveau intermédiaire

### La classe `object`

Vous pouvez trouver du code dans lequel les classes héritent de la classe
`object`, comme dans cet exemple tiré du module standard `zipfile` :


    from modtools import show_module
    import zipfile
    show_module(zipfile,beg='class ZipFile(', end="file:")

Ceci nous donne l'occasion de citer le module `zipfile`, qui permet de lire ou
écrire, de manière transparente, des fichiers compressés au format `zip`.

### Les classes *new-style*

Mais le sujet de ce complément est l'héritage entre `ZipFile` et la classe
`object`. Voici ce qu'il faut en retenir en version courte.

Aux alentours de la version 2.2 - 2.3 de python, on a amélioré le langage pour
régler quelques problèmes qui existaient dans le système de types. En substance,
et pour rester synthétique :

 * Il n'était pas possible dans les anciennes versions de spécialier un type
prédéfini. Par exemple si vous vous souvenez de la classe
`collections.OrderedDict`, il s'agit d'une spécialisation du type *builtin*
`dict`. Il n'aurait pas été possible d'implémenter cette classe avec les
anciennes versions du langage.

 * Dans l'ancien modèle mental, les classes et les types jouent un rôle
différent. Or dans la logique d'un langage orienté objet, le type d'une
instance, c'est sa classe. Nous allons y revenir avec des exemples.

Pour améliorer le langage, on a alors introduit la notion de classe *new-style*.

Pour **ne pas casser la compatibilité ascendante**, on a convenu que pour qu'une
classe soit ***new-style***, il faut qu'elle **hérite** - directement ou
indirectement - de la classe *builtin* `object`.

### Illustration

Une instance d'une classe *old-style* a pour type le type `instance` :


    # une classe old-style
    class OldStyle: pass
    # une instance
    old_style = OldStyle()
    # son type est juste 'instance'
    type(old_style)

Par contre une instance d'une classe *new-style* a pour type la classe qu'on a
utilisée pour créer l'objet :


    # une classe new-style : elle hérite de 'object'
    class NewStyle(object): pass
    # une instance
    new_style = NewStyle()
    # le type de l'instance est bien la classe
    type(new_style) is NewStyle

### Digression sur python3

En python 3, toutes les classes sont maintenant *new-style*, qu'elles héritent
ou non de `object`. C'est pourquoi il est **conseillé**, dans vos programmes
python2, de **systématiquement écrire des classes new-style**.

## Complément - niveau avancé

### Pour en savoir plus

Si ce sujet vous intéresse, vous pouvez commencer par [l'article initial de
Guido Van Rossum](https://www.python.org/download/releases/2.2.3/descrintro) au
sujet de la nouvelle implémentation.

D'autres liens pertinents sont aussi donnés [ici dans la documentation
python](https://www.python.org/doc/newstyle/).
