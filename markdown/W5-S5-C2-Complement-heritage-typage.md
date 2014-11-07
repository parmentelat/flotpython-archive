
# Héritage, typage

## Complément - niveau intermédiaire

### À quoi l'héritage **ne sert pas** en python

nous discuterons ensuite de ce pour quoi l'héritage **n'est pas fait** en
python, une section qui peut être bénéfique aux gens déjà habitués à C++ ou à
Java;

##### Familles de classe / typage

Si vous êtes familiers avec un langage statiquement typé comme C++, vous êtes
sans doute habitués à appréhender l'héritage *aussi* en terme de types.

Commençons avec un exemple simple et classique. Imaginons que l'on veuille
écrire un analyseur syntaxique pour un langage simple d'expressions
arithmétiques. En pratique cela voudra dire disposer d'un parser pour
transformer un texte comme

    (10 + 12) * (32 + 5)

en un arbre syntaxique construit avec les opérateurs `Entier`, `Plus`, `Fois`,
chacun représenté comme une classe; pour ce texte on obtiendrait donc l'objet

    Fois(Plus(Entier(10), Entier(12)), Plus(Entier(32), Entier(5)))

###### En C++

Avec un langage comme C++ à nouveau, pour implémenter ceci, on va avoir tendance
à définir un **type chapeau** qu'on appelle par exemple `Expression`, et on va
concevoir un arbre d'héritage du genre de&nbsp;:

    Expression
    |-- Entier
    |-- Plus
    |-- Fois

On n'a **pas vraiment le choix de le faire ou non**; en effet, il faut pour
satisfaire le compilateur et surtout le type-checker statique, pouvoir **donner
un type** à une fonctionnalité qui ferait l'évaluation d'une telle expression.

                class Expression {
  public:
    virtual int evaluate ()=0;
}
                
Ce faisant on indique aussi que toutes les classes filles **doivent**
implémenter la méthode en question, ce que le type-checker statique vérifiera
également.

###### En python

En python, pour résoudre ce problème, on **peut** naturellement définir la même
hiérarchie de classes. Cependant si on le fait on s'aperçoit que le gain est
somme toute très faible.


    xxxx
