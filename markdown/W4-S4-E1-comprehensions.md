
# Compréhensions

## Exercice - niveau basique

Il vous est demandé d'écrire une fonction `aplatir` qui prend *un unique*
argument `l_conteneurs`, une liste (ou plus généralement un itérable) de
conteneurs, et qui retourne la liste de tous les éléments de tous les
conteneurs.


    # par exemple
    from corrections.w4_comprehensions import exo_aplatir
    exo_aplatir.exemple()


    def aplatir(conteneurs):
        "<votre_code>"


    # vérifier votre code
    exo_aplatir.correction(aplatir)

## Exercice - niveau intermédiaire

À présent, on passe en argument deux conteneurs (deux itérables) `c1` et `c2` de
même taille à la fonction `alternat`, qui doit construire une liste contenant
les éléments pris alternativement dans `c1` et de `c2`.


    # exemple
    from corrections.w4_comprehensions import exo_alternat
    exo_alternat.exemple()


    def alternat(c1, c2):
        "<votre_code>"


    # pour vérifier votre code
    exo_alternat.correction(alternat)

## Exercice - niveau intermédiaire

On se donne deux ensembles A et B de tuples de la forme

    (entier, valeur)

On vous demande d'écrire une fonction `intersect` qui retourne l'ensemble des
objets `valeur` associés (dans A ou dans B) à un entier qui soit présent dans
(un tuple de) A *et* dans (un tuple de) B.


    # un exemple
    from corrections.w4_comprehensions import exo_intersect
    exo_intersect.exemple()


    def intersect(A, B):
        "<votre_code>"


    # pour vérifier votre code
    exo_intersect.correction(intersect)
