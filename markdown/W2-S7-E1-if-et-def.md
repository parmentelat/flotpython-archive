
# Instruction `if` et fonction `def`

## Exercices - niveau basique

### Fonction de divisibilité

L'exercice consiste à écrire une fonction baptisée `divisible` qui retourne une
valeur booléenne qui indique si un des deux arguments est divisible par l'autre.

Vous pouvez supposer les entrées `a` et `b` entiers et non nuls, mais pas
forcément positifs.


    def divisible(a, b):
        "<votre_code>"

Vous pouvez à présent tester votre code en évaluant ceci, qui écrira un message
d'erreur si un des jeux de test ne donne pas le résultat attendu.


    # tester votre code
    from corrections.w2_if import exo_divisible
    exo_divisible.correction(divisible)

**Remarque.** Vu comme le problème est posé, il est assez naturel d'utiliser un
`if` pour écrire 'divisible'. Vous remarquerez toutefois qu'un `if` n'est pas
strictement indispensable, et nous vous invitons à exhiber une version sans `if`
qui est plus pythonique.

### Manipulation de liste

Cet exercice consiste à écrire une fonction `spam`, qui prend en argument une
liste, et qui retourne la liste modifiée comme suit:
 * si la liste est de taille paire, on intervertit les deux premiers éléments de
la liste,
 * si elle est de taille impaire, on lui retire son dernier élément.


    # pour la correction et un exemple
    from corrections.w2_if import exo_spam


    # voici quelques exemples de ce qui est attendu
    exo_spam.exemple()


    # écrivez votre code 
    def spam(liste):
        "<votre_code>"


    # pour le vérifier, évaluez cette cellule
    exo_spam.correction(spam)
