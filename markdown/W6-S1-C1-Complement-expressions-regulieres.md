
# Expressions régulières

## Complément - niveau intermédiaire

Le langage perl avait été le premier à populariser l'utilisation des expressions
régulières, en en faisant un "citoyen de première classe" dans le langage
(c'est-à-dire supporté nativement dans le langage, et non au travers d'une
librairie).

En python, les expressions régulières sont disponibles de manière plus
traditionnelle, via le module `re` de la librairie standard, dont nous allons
dire quelques mots.

### Avertissement


    xxx dépendant du locale

### Un exemple simple

Je vous conseille d'avoir sous la main la [documentation du module
`re`](https://docs.python.org/2/library/re.html) pendant que vous lisez ce
complément.


    import re


    sentences = [u'Lacus donec vitae porta gravida proin donec sociis.', u'Neque ipsum rhoncus cras quam.']
    l1, l2 = sentences

On peut chercher toutes les mots se terminant par a ou e dans une ligne en
faisant&nbsp;:


    re.findall (r"\w+[ae][^\w]", l1)

Ce code permer de chercher dans la chaîne `l1` toutes (`findall`) les
occurrences de l'expression régulière, qui ici est le *raw-string* c'est-à-dire
la chaîne

    `r"\w+[ae][^\w]"`.

Nous verrons tout à l'heure comment fabriquer des expressions régulières plus en
détail, mais pour démystifier au moins celle-ci&nbsp;:
 * `\w+` : il nous faut trouver une sous-chaîne qui commence par un nombre
quelconque, mais au moins égal à 1, de
