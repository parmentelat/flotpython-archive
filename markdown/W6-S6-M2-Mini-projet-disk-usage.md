
# Utilisation du disque dur

## Mini-Projet

### Introduction

De temps en temps vous vous rendez compte que votre disque dur est plein ou que
vous avez rempli votre quota.
En application de la loi de Murphy, en général c'est à un mauvais moment; il est
vrai qu'on a toujours mieux à faire que de nettoyer un disque.

### Objectifs

Dans ce mini-projet nous allons écrire un utilitaire permettant de nous aider
dans ce genre de situations. Les objectifs que l'on pourrait avoir sont&nbsp;:
 * de trouver rapidement les gros répertoires, en partant d'une racine ou d'un
répertoire utilisateur;
 * de stocker les données de taille de façon à ne pas avoir à attendre plusieurs
minutes à recalculer sans cesse les tailles des différents morceaux;
 * et notamment de pouvoir lancer toutes les nuits un scan silencieux, de façon
à avoir immédiatement, dans la journée, accès à des informations - même
approchées - de nature à identifier le ou les répertoires qui pose problème ou
qui a un fort potentiel de libération d'espace.

### Approche

Pour cela on conçoit un système simple qui fonctionne en deux passes&nbsp;:
 * une première passe de type *batch* qui stocke dans chaque répertoire, dans un
fichier spécial (nous avons utilisé le nom `.du`) la taille totale de ce
répertoire,
 * une seconde passe interactive, qui peut
   * afficher les tailles des sous-répertoires triés, précisément, par taille,
   * naviguer dans les répertoires sur cette base,
   * et procéder au nettoyage proprement dit.

Aussi voici les choix que j'ai faits pour mon implémentation&nbsp;:
 * un seul module qui contient tout le programme, et qui s'appelle
`diskusage.py`
 * par défaut le programme ne lance que la seconde passe
 * on peut ne lancer que la première passe avec l'option `-1`
 * ou les deux passes en séquence avec l'option `--both`

Voici l'aide en ligne

***

    $ diskusage.py --help
    usage: diskusage.py [-h] [-1] [-b] [-v] dir

    positional arguments:
      dir

    optional arguments:
      -h, --help         show this help message and exit
      -1, --pass1        Run pass1, that computes .du in all subdirs
      -b, --both-passes  Run pass1, that computes .du in all subdirs,
                         and then pass2 that is interactive
      -v, --verbose      turn on verbose output

***

Vous reconnaissez sans doute l'utilisation à nouveau de `ArgumentParser` importé
du module `argparse` pour la définition de la syntaxe d'appel de `diskusage.py`

### Exemple d'utilisation

Nous publions un directory de test pour vous permettre de vérifier vos
résultats, comme d'habitude
dans les formats suivants&nbsp;:
 * [format tar](data/diskusage-spam.tar)
 * [format tgz](data/diskusage-spam.tgz)
 * [format zip](data/diskusage-spam.zip)

qui donne une structure de fichiers telles que ceci&nbsp;:

<img src="media/diskusage-spam.png">

##### La première passe

Si j'installe cette structure sur mon propre disque, voici ce que
j'obtiens&nbsp;:

    % diskusage.py spam
    Welcome to inspection of path spam
    -------- Path spam has a total size of xxx 0 xxx
    1    xxx 0 xxx   big
    2    xxx 0 xxx   little
    3    xxx 0 xxx   medium
    4    xxx 0 xxx   small
    Enter number (h for help) q
    %

Ce qui est 'normal' ou en tous cas attendu, car je n'ai pas lancé la première
passe:

    % find spam -name .du
    % diskusage.py -1 spam
    %

##### La deuxième passe

Maintenant si je recommence, l'outil me montre les directories triés par taille,
le plus gros en dernier - parce que c'est sans doute celui qui m'intéresse le
plus&nbsp;:

    % diskusage.py spam
    Welcome to inspection of path spam
    -------- Path spam has a total size of 3.16 MiB
    1     1.15 KiB   little
    2   139.73 KiB   small
    3     1.09 MiB   medium
    4     1.93 MiB   big
    Enter number (h for help)

À ce stade-là je peux naviguer dans l'arbre en utilisant&nbsp;:

 * soit un nombre pour me déplacer dans l'arbre

    Enter number (h for help) 2
    -------- Path spam/small has a total size of 139.73 KiB
    Enter number (h for help)

 * soit `u` ou `..` pour remonter

    Enter number (h for help) u
    -------- Path spam has a total size of 3.16 MiB
    1     1.15 KiB   little
    2   139.73 KiB   small
    3     1.09 MiB   medium
    4     1.93 MiB   big
    Enter number (h for help)

 * soit '+' (ou une ligne vide) pour choisir le répertoire le plus gros

     Enter number (h for help)
    -------- Path spam/big has a total size of 1.93 MiB
    1         68 B   empty
    2     4.60 KiB   f
    3   126.17 KiB   d
    4   252.17 KiB   b
    5   558.23 KiB   a
    6  1008.17 KiB   c
    Enter number (h for help)

 * soit `l` pour lister les **fichiers** (jusqu'ici la commande n'a listé que
des répertoires)

     Enter number (h for help) l
    ---- Plain files in spam/big
    F          8 B   .du
    F        576 B   zfile-01
    F     1.12 KiB   zfile-02
    F     2.25 KiB   zfile-03
    F     4.50 KiB   zfile-04
    F     6.00 KiB   .DS_Store
    F        9 KiB   zfile-05
    Enter number (h for help)

 * voici d'ailleurs l'aide en ligne

    Enter number (h for help) h
    num go to listed directory
    +   (default) go to last (and thus biggest) directory
    u   go one step up - can be also '0' or '..'
    l   list files in the current directory
    .   come again (stay in place)
    !   re-run pass1
    v   toggle verbose on and off
    q   quit
    h   this help

### Que faut-il faire au juste ?

Tout ce qui précède vous est donné à titre purement indicatif, pour vous décrire
ce que fait l'implémentation qui sera donnée comme corrigé de cet exercice.

Gardez bien présent à l'esprit toutefois qu'il ne s'agit pas d'une évaluation,
aussi vous pouvez librement vous inspirer de cette implémentation. Dans l'état
que je viens de décrire, l'outil est passif (il ne permet pas de détruire des
fichiers), mais relativement exhaustif (vous pouvez voir toutes les tailles de
tous les répertoires et de tous les fichiers). À vous de choisir l'étendue de ce
que vous voulez faire.

Une variante **plus simple** consisterait à se contenter de ne montrer que les
répertoires, puisqu'en général une fois qu'on a isolé le répertoire on peut
utiliser un navigateur de fichiers plus classique.

Une variante **plus compliquée** consisterait à permettre des destructions de
fichiers ou de répertoires nativement dans l'outil. Dans ce cas il serait bon de
mettre à jour les tailles enregistrées dans les `.du`.

De même ma version incorpore un mode bavard (*verbose*); lorsqu'il est activé on
peut montrer plus de détails sur le fonctionnement interne de l'outil, par
exemple en imprimant une ligne à chaque fois qu'on calcule vraiment la taille
d'un répertoire - pour mieux comprendre ce qui se passe. Bien entendu pour
commencer vous ne prévoyez pas de mode bavard.

De même vous voyez dans l'aide en ligne quelques utilitaires supplémentaires,
comme notamment `!` pour recalculer les tailles à partir de l'état du disque. En
principe, ajouter ce genre de features ne prend que quelques lignes de code,
mais là encore c'est à vous de voir.

Enfin, le code étant extrêmement basique en termes d'utilisation de librairies,
je vous propose si vous avez le temps d'essayer de faire fonctionner votre code
aussi en python3 - c'est-à-dire, une fois que votre code fonctionne en python2,
d'essayer de le modifier à la marge pour obtenir un code unique qui fonctionne
avec les deux versions. Pour cela attendez tout de même d'avoir lu le complément
que nous consacrons à ce sujet en Semaine 7.

### Quelques indices

Une des difficultés de cet exercice est de gérer le fait que le système est
'vivant' pendant la sesssion; aussi les données cachées dans les `.du` peuvent
être anciennes. Ces deux facteurs font qu'il se peut que certains répertoires
ont un `.du` et pas d'autres. Ici j'ai adopté une stratégie simple qui est de
retourner une taille nulle (pour pouvoir tout de même afficher le résultat de la
somme) et de faire en sorte que l'impression d'une taille nulle attire l'oeil
(voir le tout premier exemple ci-dessus).

Notez aussi, pour ceux qui n'y sont pas habitués, qu'**un répertoire a une
taille propre**. Du point de vue de l'utilisateur un répertoire ne contient
'rien' mais il faut de la place pour ranger les noms des fichiers. C'est en
général négligeable, mais avec un grand nombre de petits fichiers c'est mieux
d'en tenir compte.

Si vous voulez aborder l'exercice dans une optique 'niveau avancé', vous pouvez
vous arrêter là, et essayer d'implémenter l'outil sans plus d'indications.

##### Librairies

En termes de librairies tierces, c'est difficile de faire plus simple; mon
implémentation utilise uniquement&nbsp;:
 * `os` et spécifiquement `os.walk`, `os.listdir`,
 * `os.path` et dans ce module `join`, `getsize`, `exists`, `isdir`, `isfile`,
`dirname`,
 * et donc `argparse.ArgumentParser`.
