
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

Voici deux exemples de chaînes.


    sentences = ['Lacus a donec, vitae porta gravida:; proin donec sociis.', 
                 'Neque ipsum! rhoncus cras quam.']

##### `findall`

On peut chercher tous les mots se terminant par a ou m dans une chaîne en
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

##### `split`

Une autre forme simple d'utilisation des regexps est `re.split`, qui fournit une
fonctionnalité voisine de `str.split` qu'on a vue en semaine 2, mais ou les
séparateurs sont exprimés comme une expression régulière; ou encore on peut le
voir un peu comme la négation de `findall`&nbsp;:


    for sentence in sentences:
        print 4*'-','dans >{}<'.format(sentence)
        print re.split (r"\W+", sentence)

Ici l'expression régulière, qui donc décrit le séparateur, est simplement `\W+`
c'est-à-dire toute suite d'au moins caractère non alphanumérique.

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

Nous allons maintenant voir comment on peut, d'abord vérifier si une chaîne est
conforme au critère défini par l'expression régulière, mais aussi *extraire* les
morceaux de la chaîne qui correspondent aux différentes parties de l'expression.

Pour cela supposons qu'on s'intéresse aux chaînes qui comportent 5 parties, une
suite de chiffres, une suite de lettres, des chiffres à nouveau, des lettres, et
enfin de nouveau des chiffres.

Avec ces deux chaines en entrée&nbsp;:


    inputs = [ '890hj000nnm890',    # cette entrée convient
               '123abc456def789',   # celle-ci aussi
               '8090abababab879',   # celle-ci non
               ]

Pour commencer, voyons que l'on peut facilement vérifier si une chaîne vérifie
ou non ce critère&nbsp;:


    regexp1 = "[0-9]+[A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"

Ce qui nous donne


    for input in inputs:
        print '---> input',input
        print re.match(regexp1, input)

Ici plutôt que d'utiliser les raccourcis comme `\w` j'ai préféré écrire
explicitement les ensembles de caractères en jeu; ce cette façon on rend son
code indépendant du LOCALE si c'est ce qu'on veut faire. Il y a deux morceaux
qui interviennent tour à tour&nbsp;:
 * `[0-9]+` signifie une suite de au moins un caractère dans l'intervalle
`[0-9]`,
 * `[A-Za-z]+` pour une suite d'au moins un caractère dans l'intervalle `[A-Z]`
ou dans l'intervalle `[a-z]`.

##### Nommer un morceau (un groupe)


    # on se concentre sur une entrée correcte
    haystack = inputs[1]
    haystack

Maintenant, on va même pouvoir donner un nom à un morceau de la regexp, ici
`needle`


    # la même regexp, mais on donne un nom à un morceau
    regexp2 = "[0-9]+[A-Za-z]+(?P<needle>[0-9]+)[A-Za-z]+[0-9]+"

Et une fois que c'est fait on peut demander à l'outil de nous retrouver la
partie correspondante dans la chaine initiale&nbsp;:


    print re.match(regexp2, haystack).group('needle')

Dans cette expression on a utilisé un **groupe nommé** `(?P<needle>[0-9]+)`.

### Un troisième exemple

Enfin, et c'est un trait qui n'est pas présent dans tous les langages, on peut
restreindre un morceau de chaîne à être identique à un groupe déjà vu avant dans
la chaîne; dans l'exemple ci-dessus on pourrait ajouter comme contrainte que le
premier et le dernier groupes de chiffres soient identiques comme ceci&nbsp;:


    regexp = "(?P<id>[0-9]+)[A-Za-z]+(?P<needle>[0-9]+)[A-Za-z]+(?P=id)"

Avec les mêmes entrées que tout à l'heure


    for input in inputs:
        print '---> input',input
        print re.match(regexp, input)

La nouveauté ici est la **backreference** `(?P=id)`.

### Comment construire une expression régulière

Nous pouvons à présent refaire une liste des constructions qui permettent
d'élaborer une expression régulière, en restant toutefois synthétique puisque la
[documentation du module `re`](https://docs.python.org/2/library/re.html) en
donne une version exhaustive.

##### La brique de base : le caractère

Au commencement il faut spécifier des caractères&nbsp;:
 * **un seul** caractère : vous le citez tel quel, en le précédent d'un
backslash `\` s'il a par ailleurs un sens spécial dans le micro-langage de
regexps (comme `+`, `*`, `[` et autres ...);
 * **un ensemble** de caractères avec la notation `[...]` qui permet de décrire
   * ex. `[a1=]` : un ensemble in extenso, ici un caractère parmi les 3: `a`,
`1`, ou `=`,
   * ex. `[a-z]` : un intervalle de caractères
   * ex. `[15e-g]` : un mélange des deux, qui contiendrait ici `1`, `5`, `e`,
`f` et `g`
   * ex. `[^15e-g]` : une négation, qui a `^` comme premier caractère dans les
`[]`, ici tout sauf l'ensemble précédent;
 * un ensemble de caractères prédéfini, qui peuvent alors dépendre de
l'environnement (i.e. UNICODE et LOCALE) avec les notations&nbsp;:
   * `\w` les caractères alphanumériques, et `\W` (les autres),
   * `\s` les caractères "blancs" - espace, tabulation, saut de ligne, etc...,
et `\S` (les autres),
   * `\d` pour les chiffres, et `\D` (les autres),


##### En série ou en parallèle

Si je fais une analogie avec les montages électriques, jusqu'ici on a vu le
montage en série&nbsp;: on met des expressions régulières bout à bout, qui
matchent la chaine en entrée séquentiellement du début à la fin. On a *un peu*
de marge pour spécifier des alternatives, lorsqu'on fait par exemple

    "ab[cd]ef"

mais c'est limité à **un seul** caractère. Si on veut reconnaitre deux mots qui
n'ont pas grand-chose à voir comme `abc` **ou** `def`, il faut en quelque sorte
mettre deux regexps en parallèle, et c'est ce que permet l'opérateur `|`


    for input in [ 'abc', 'def', 'xxx' ]:
        print input, re.match("abc|def", input)

##### Fin(s) de chaîne

Selon que vous utilisez `match` ou `search`, vous précisez si vous vous
intéressez uniquement à un match en début (`match`) ou n'importe où (`search`)
dans la chaîne.

Mais indépendamment de cela, il peut être intéressant de "coller" l'expression
en début ou en fin de ligne, et pour ça il existe des caractères spéciaux&nbsp:;
 * `^` lorsqu'il est utilisé comme un caractère (c'est à dire pas en début de
`[]`) signifie un début de chaîne;
 * `\A` a le même sens (sauf en mode MULTILINE), et je le recommande de
préférence à `^`qui est déjà pas mal surchargé;
 * `$` matche une fin de ligne;
 * `\Z` est voisin mais pas tout à fait identique.

Reportez-vous à la documentation pour le détails des différences.

##### Parenthéser - (grouper)

Du coup pour pouvoir faire des montages élaborés il faut pouvoir
parenthéser&nbsp;:


    for input in [ 'abcf', 'adef', 'abf' ]:
        print input, re.match("a(bc|de)f", input)

##### Comment compter

Vous disposez des opérateurs suivants&nbsp;:
 * ex. `(ab)*` l'étoile `*` qui signifie n'importe quel nombre, même nul,
d'occurrences,
 * ex. `(ab)+` le plus `+` qui signifie au moins une occurrence
 * ex. `(ab){3}` pour exactement 3 occurrences de `(ab)`, ici ce serait
exactement équivalent à `ababab`
 * ex. `(ab){3,4}` entre 3 et 4 fois


    inputs = [ n*'ab'for n in [0, 1, 3, 4]] + [ 'foo' ]
    
    for regexp in [ '(ab)*', '(ab)+', '(ab){3}', '(ab){3,4}' ]:
        # on ajoute \A \Z pour matcher toute la chaine
        line_regexp = r"\A{}\Z".format(regexp)
        for input in inputs:
            print 'RE', line_regexp, 'INPUT', input, '->', re.match(line_regexp, input)

### Greedy *vs* non-greedy

****

On peut mettre un "\n" comme caractère (et faire des RE multilignes)


    lexer + parser 
