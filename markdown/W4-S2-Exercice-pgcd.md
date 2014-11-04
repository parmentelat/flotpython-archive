
# Calculer le PGCD

## Exercice - niveau basique

On vous demande d'écrire une fonction qui calcule le pgcd de deux entiers, en
utilisant [l'algorithme
d'Euclide](http://fr.wikipedia.org/wiki/Algorithme_d'Euclide).

def pgcd(a, b):
    "<votre code>"


    # pour vérifier votre code
    from corrections.w4_pgcd import exo_pgcd
    exo_pgcd.correction(pgcd)

**Remarque** on peut tout à fait utiliser une fonction récursive pour
implémenter l'algorithme d'Euclide. Par exemple cette version de `pgcd`
fonctionne très bien aussi (en supposant a>=b)

    def pgcd(a, b):
       "Le pgcd avec une fonction récursive"
       if not b:
           return a
       return pgcd(b, a % b)

Cependant, il vous est demandé ici d'utiliser une boucle `while`, qui est le
sujet de la séquence, pour implémenter `pgcd`.

