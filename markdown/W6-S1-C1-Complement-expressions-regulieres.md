
# Expressions régulières

## Complément - niveau intermédiaire

Le langage perl avait été le premier à populariser l'utilisation des expressions
régulières, en en faisant un "citoyen de première classe" dans le langage
(c'est-à-dire supporté nativement dans le langage, et non au travers d'une
librairie).

En python, les expressions régulières sont disponibles de manière plus
traditionnelle, via le module `re` de la librairie standard, dont nous allons
dire quelques mots.


    import re

Je vous conseille d'avoir sous la main la [documentation du module
`re`](https://docs.python.org/2/library/re.html) pendant que vous lisez ce
complément.

### Avertissement

Dans ce complément nous serons amenés à utiliser des traits qui dépendent du
LOCALE, c'est-à-dire pour faire simple de comment un ordinateur est configuré
vis-à-vis de la langue.

Tant que vous exécutez ceci dans le notebook sur la plateforme, en principe tout
le monde verra exactement la même chose. Par contre si vous faites tourner le
même code sur votre ordinateur, il se peut que vous obteniez des résultats
différents.

### Un exemple simple


    sentences = [u'Lacus a donec vitae porta gravida proin donec sociis.', 
                 u'Neque ipsum rhoncus cras quam.']

On peut chercher toutes les mots se terminant par a ou m dans une chaîne en
faisant&nbsp;:


    for sentence in sentences:
        print 4*'-','dans >{}<'.format(sentence)
        print re.findall (r"\w*[am]\W", sentence)

Ce code permet de chercher toutes (`findall`) les occurrences de l'expression
régulière, qui ici est le *raw-string* c'est-à-dire la chaîne

    `r"\w*[am]\W"`

Nous verrons tout à l'heure comment fabriquer des expressions régulières plus en
détail, mais pour démystifier au moins celle-ci, on a mis bout à bout des
morceaux d'expression régulières&nbsp;:
 * `\w*` : il nous faut trouver une sous-chaîne qui commence par un nombre
quelconque, y compris nul, de caractères alphanumériques; ceci est défini en
fonction de votre LOCALE, on y reviendra;
 * `[am]` : immédiatement après, il nous faut trouver un caratère `a` ou `m`;
 * `\W` : et enfin, il nous faut un caractère qui ne soit pas alphanumérique.

##### Pourquoi un *raw-string* ?

En guise de digression, il n'y a aucune obligation à utiliser un *raw-string*;
d'ailleurs il n'y a pas de différence de nature entre un *raw-string* et une
chaîne usuelle&nbsp;:


    raw = r'abc'
    regular = 'abc'
    # comme on a pris une 'petite' chaîne ce sont les mêmes objets
    print 'is', raw is regular
    # et donc a fortiori
    print '==', raw == regular

Il se trouve que, comme dans notre premier exemple, le *backslash* `\` à
l'intérieur des expressions régulières est d'un usage assez courant. C'est
pourquoi on **utilise fréquemment un *raw-string*** pour décrire une expression
régulière.

### Un deuxième exemple

Nous allons maintenant voir comment on peut, vérifier si une chaîne est conforme
au critère défini par l'expression régulière, mais aussi *extraire* les morceaux
de la chaîne qui correspondent aux différentes parties de l'expression.

Pour cela supposons qu'on s'intéresse aux chaînes qui comportent 5 parties, une
suite de chiffres, une suite de lettres, des chiffres à nouveau, des lettres, et
enfin de nouveau des chiffres.

Avec ces deux chaines en entrée&nbsp;:


    inputs = [ '890hj000nnm890',    # cette entrée convient
               '8090abababab879',   # celle-ci non
               ]

Pour commencer, voyons que l'on peut facilement vérifier si une chaîne vérifie
ou non ce critère&nbsp;:


    regexp = "[0-9]+[A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"
    
    for input in inputs:
        print '---> input',input
        print re.match(regexp, input)

Ici plutôt que d'utiliser les raccourcis comme `\w` j'ai préféré écrire
explicitement les ensembles de caractères en jeu; ce cette façon on rend son
code indépendant du LOCALE si c'est ce qu'on veut faire. Il y a deux morceaux
qui interviennent tour à tour&nbsp;:
 * `[0-9]+` signifie une suite de au moins un caractère dans l'intervalle
`[0-9]`,
 * `[A-Za-z]+` pour une suite d'au moins un caractère dans l'intervalle `[A-Z]`
ou dans l'intervalle `[a-z]`.

##### Nommer un morceau


    # on se concentre sur l'entrée correcte
    haystack = inputs[0]

Maintenant, on va même pouvoir donner un nom à un morceau de la regexp, ici
`needle`.


    # la même regexp, mais on donne un nom à un morceau
    regexp = "[0-9]+[A-Za-z]+(?P<needle>[0-9]+)[A-Za-z]+[0-9]+"

Et une fois que c'est fait on peut demander à l'outil de nous retrouver la
partie correspondante dans la chaine initiale&nbsp;:


    print re.match(regexp, haystack).group('needle')

****

On peut mettre un "\n" comme caractère (et faire des RE multilignes)
