
# Les chaînes de caractères

## Exercices - niveau basique

### Analyse et mise en forme

Un fichier contient, dans chaque ligne, des informations (champs) séparées par
des virgules.
Les espaces et tabulations présentes dans la ligne ne sont pas significatifs et
doivent être ignorés. Il arrive que certaines lignes se terminent par une
virgule, une fois les espaces ignorés.

Le premier et deuxième champs représentent le prénom et le nom de la personne,
respectivement. Lorsque la ligne contient au moins 4 champs, alors ce 4ème
champs représente l'âge de la personne.

On vous demande d'écrire la fonction `affichage`, qui analyse une ligne, et qui
 * prend en argument une ligne (chaîne de caractères)
 * retourne une chaîne de caractères mise en forme (voir exemples)
 * ou bien retourne None si la ligne n'a pas pu être analysée


    # pour la correction, et l'exemple
    from corrections.w2_strings import exo_affichage


    # voici quelques exemples de ce qui est attendu
    exo_affichage.exemple()


    # écrivez votre code ici
    def affichage(ligne):
        "<votre_code>"


    # pour le vérifier
    exo_affichage.correction(affichage)

### Mise au carré

On vous demande à présent d'écrire une fonction dans le même esprit que ci-
dessus.
Cette fois, chaque ligne contient, séparés par des point-virgules, une liste
d'entiers, et on veut obtenir une nouvelle chaîne avec les carrés de ces
entiers, séparés par des deux-points.

Comme ci-dessus les lignes peuvent être remplies de manière approximative, avec
des espaces, des tabulations, ou même des points-virgules en trop, que ce soit
au début, à la fin, ou au milieu d'une ligne


    # pour la correction, et l'exemple
    from corrections.w2_strings import exo_carre


    # exemples
    exo_carre.exemple()


    # écrivez votre code ici
    def carre(ligne):
        "<votre_code>"


    # pour corriger
    exo_carre.correction(carre)
