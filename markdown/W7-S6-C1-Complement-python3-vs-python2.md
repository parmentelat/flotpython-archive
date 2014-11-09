
# python3 vs python2

## Complément - niveau intermédiaire

Comme promis en Semaine 1, et maintenant que vous avez une vision d'ensemble de
python2, voici un complément consacré à python3. Nous aborderons cette question
selon deux angles&nbsp;:
 * pour commencer nous ferons un résumé des différences entre les deux langages,
 * et nous tenterons de faire le point sur la migration entre les deux versions.

Dans l'introduction de la Semaine 1, nous avons indiqué avoir choisi de
concentrer le cours sur python2 car c'est encore aujourd'hui la version
dominante du langage. Vous [pourrez lire ici](https://wiki.python.org/moin/2.x-v
s-3.x-survey?action=AttachFile&do=view&target=2013-2014+Python+2.x-3.x+survey.pd
f)
 les résultats d'[un sondage fait fin 2013/début
2014](https://wiki.python.org/moin/2.x-vs-3.x-survey) qui le démontre assez
nettement, même si les choses semblent bouger comme on le verra plus bas.

### Les différences

Pendant toute la maturation de python, au moins depuis l'introduction de python2
en 2000, toutes les évolutions ont été faites avec compatibilité ascendante, et
vous pouvez en théorie faire tourner du code 2.1 dans un interprèteur 2.7. Avec
cette approche il n'est naturellement pas possible d'enlever ou de changer les
traits du langages qui ont été ratés :)

La décision de créer python3 a été prise dans le but de corriger ce genre de
défauts, avec en contrepartie la nécessité de migrer tout la base de code.
Commençons par faire un survol des changements, avant de voir dans la deuxième
partie comment se passe cette migration.

##### `print`

On a déjà eu l'occasion de l'évoquer, la différence la plus visible entre les
deux versions du langage est que
 * dans python2 `print` est une **instruction** et ne prend pas de parenthèse,
 * alors qu'en python3 c'est une **fonction** et donc requiert des parenthèses.

Comme on l'avait signalé en Semaine 1 (Séquence "Pourquoi python ?"), vous avez
la possibilité d'écrire du code python2 qui utilise `print` avec la syntaxe de
python3 en mentionnant

    from __future__ import print_function

Cela dit, `print` est une construction très visible pendant la période
d'apprentissage, mais dans du vrai code son usage est **beaucoup moins répandu**
qu'on ne pourrait le penser, on utilise la plupart du temps des modules de
`logging` ou autres fonctions d'écriture sur fichier, aussi l'évolution de
`print` est en réalité beaucoup moins cruciale qu'il n'y paraît.

##### types `str` et `unicode`

Le changement le plus radical, dans le sens, le changement auquel il est le plus
délicat de s'adapter, est sans doute celui qui

<pre style="font-size:small;background-color:'#ccc';">
Everything you thought you knew about binary data and Unicode has changed.
</pre>


##### types `int` et `long`

##### classes *new-style*

https://docs.python.org/3/whatsnew/3.0.html#text-vs-data-instead-of-unicode-
vs-8-bit

##### Variables locales à une boucle `for`

##### Autres changements

Citons également, en vrac&nbsp;:
 * la possibilité d'annoter au niveau syntaxique les arguments et valeur de
retour des fonctions ([voir PEP3107](http://www.python.org/dev/peps/pep-3107));
dans l'état actuel il s'agit d'annotations à vocation **surtout documentaire**
et il ne semble pas que le langage se dirige vers un contrôle de type plus
strict dans ce domaine;
 * une nouvelle notation pour spécifier la métaclasse;
 * et tout un tas d'autres améliorations moins significatives, dont vous
trouverez [une liste plus exhaustive
ici](https://docs.python.org/3/whatsnew/3.0.html).

Signalons enfin l'existence d'un [guide pour le portage de python2 à
python3](https://docs.python.org/3/howto/pyporting.html)

### Un point sur la migration

##### 2to3

##### six

##### timeframe

##### django/numpy available (since when ?)

### Pour en savoir plus

 * https://wiki.python.org/moin/Python2orPython3

