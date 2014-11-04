
# Héritage

xxx
j'ai beacoup de mal avec ce complément - je passe pour l'instant
xxx

## Complément - niveau basique

### À quoi sert l'héritage en python ?

La notion d'héritage, qui fait partie intégrante de la Programmation Orientée
Objet, permet principalement de maximiser la **réutilisabilité**.

Nous avons vu dans la vidéo les mécanismes d'héritage *in abstracto*. Pour
résumer très brièvement, on recherche un attribut (souvent une méthode) à partir
d'une instance en cherchant :
 * d'abord dans l'instance elle-même,
 * puis dans la classe de l'instance,
 * puis dans les super-classes de la classe.

Le propos de ce complément est de montrer, sur des **exemples extraits de code
réel**, comment ces mécanismes permettent en effet de contribuer à la
réutilisabilité du code.

### Factorisation de code

##### Le module `calendar`

On trouve dans la librairie standard [le module
`calendar`](https://docs.python.org/2/library/calendar.html).
Ce module expose deux classes `TextCalendar` et `HTMLCalendar`. Sans entrer du
tout dans le détail, ces deux classes permettent d'imprimer dans des formats
différents, le même type d'informations du type rendez-vous.

Le point ici est que les concepteurs ont choisi un graphe d'héritage comme ceci

    Calendar
    |-- TextCalendar
    |-- HTMLCalendar

qui permet de grouper le code concernant la logique dans la classe `Calendar`,
puis dans les deux sous-classes d'implémenter le type de sortie qui va bien.

De cette manière le maximum de code est partagé entre les deux classes; et de
plus si vous avez besoin d'une sortie au format, disons PDF, vous pouvez
envisager d'hériter de `Calendar` et n'implémenter que la partie spécifique au
format PDF.

C'est un peu le niveau élémentaire de l'héritage.

##### Le module `SocketServer`

Toujours dans la librairie standard, le [module
`SocketServer`](https://docs.python.org/2/library/socketserver.html) - qui,
incidemment est écrit en C - fait un usage beaucoup plus sophistiqué de
l'héritage.

Le module propose une hiérarchie de classes comme ceci:

                +------------+
| BaseServer |
+------------+
      |
      v
+-----------+        +------------------+
| TCPServer |------->| UnixStreamServer |
+-----------+        +------------------+
      |
      v
+-----------+        +--------------------+
| UDPServer |------->| UnixDatagramServer |
+-----------+        +--------------------+
                
Ici encore notre propos n'est pas d'entrer dans les détails, mais d'observer le
fait que les différents *niveaux d'intelligence* sont ajoutés les uns aux les
autres au fur et à mesure que l'on descend le graphe d'héritage. Ainsi un objet
de la classe `BaseServer` xxx

https://docs.python.org/2/library/socketserver.html#examples


    import BaseHTTPServer
    help (BaseHTTPServer)


    Voir aussi http://www.pasteur.fr/formation/infobio/python/ch19s04.html

##### Spécialisation

##### Composition (plutôt dire aggrégation ?)

## Complément - niveau intermédiaire

### À quoi l'héritage ne sert pas en python

##### Familles de classe / typage

Si vous êtes habitués à coder dans un langage fortement typé comme C++, vous
êtes sans doute habitués à appréhender l'héritage *aussi* en terme de types.

Voyons ceci sur un exemple. Imaginons que l'on veuille écrire un analyseur
syntaxique pour un langage simple d'expressions arithmétiques. Un pratique cela
voudra dire disposer d'un parser pour transformer un texte comme

    (10 + 12) * (32 + 5)

en un arbre syntaxique construit avec les opérateurs `Entier`, `Plus`, `Fois`,
chacun représenté comme une classe; pour ce texte on obtiendrait donc l'objet

    Fois(Plus(Entier(10), Entier(12)), Plus(Entier(32), Entier(5)))


    Avec un langage fortement typé on va avoir tendance à définir un type *chapeau* qu'on appelle par exemple `Expression`, et on va concevoir un arbre d'héritage du genre de
    
        Expression
        |-- Entier
        |-- Plus
        |-- Fois
        
    De cette façon on pourra 
