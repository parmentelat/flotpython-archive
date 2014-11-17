
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

On peut **chercher tous** les mots se terminant par a ou m dans une chaîne en
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
**fonctionnalité voisine de `str.split`** qu'on a vue en semaine 2, mais ou les
séparateurs sont exprimés comme une expression régulière; ou encore on peut le
voir un peu comme la négation de `findall`&nbsp;:


    for sentence in sentences:
        print 4*'-','dans >{}<'.format(sentence)
        print re.split (r"\W+", sentence)

Ici l'expression régulière, qui donc décrit le séparateur, est simplement `\W+`
c'est-à-dire toute suite d'au moins caractère non alphanumérique.

##### Pourquoi un *raw-string* ?

En guise de digression, il n'y a aucune obligation à utiliser un *raw-string*;
d'ailleurs on rappelle qu'il n'y a pas de différence de nature entre un *raw-
string* et une chaîne usuelle&nbsp;:


    raw = r'abc'
    regular = 'abc'
    # comme on a pris une 'petite' chaîne ce sont les mêmes objets
    print 'is', raw is regular
    # et donc a fortiori
    print '==', raw == regular

Il se trouve que, comme dans notre premier exemple, le *backslash* `\` à
l'intérieur des expressions régulières est d'un usage assez courant. C'est
pourquoi on **utilise fréquemment un *raw-string*** pour décrire une expression
régulière, et en général à chaque fois qu'elle comporte un *backslash*.

### Un deuxième exemple

Nous allons maintenant voir comment on peut, d'abord vérifier si une chaîne est
conforme au critère défini par l'expression régulière, mais aussi *extraire* les
morceaux de la chaîne qui correspondent aux différentes parties de l'expression.

Pour cela supposons qu'on s'intéresse aux chaînes qui comportent 5 parties, une
suite de chiffres, une suite de lettres, des chiffres à nouveau, des lettres, et
enfin de nouveau des chiffres.

Avec ces trois chaines en entrée&nbsp;:


    inputs = [ '890hj000nnm890',    # cette entrée convient
               '123abc456def789',   # celle-ci aussi
               '8090abababab879',   # celle-ci non
               ]

##### `match`

Pour commencer, voyons que l'on peut facilement vérifier si une chaîne vérifie
ou non ce critère&nbsp;:


    regexp1 = "[0-9]+[A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"

Ce qui nous donne


    for input in inputs:
        print 'input',input, "--> \t",
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
        print 'input',input,"-->\t",
        print re.match(regexp, input)

La nouveauté ici est la **backreference** `(?P=id)`.

### Comment construire une expression régulière

Nous pouvons à présent refaire une liste des constructions qui permettent
d'élaborer une expression régulière, en restant toutefois synthétique puisque la
[documentation du module `re`](https://docs.python.org/2/library/re.html) en
donne une version exhaustive.

##### La brique de base : le caractère

Au commencement il faut spécifier des caractères&nbsp;:
 * **un seul** caractère :
   * vous le citez tel quel, en le précédent d'un backslash `\` s'il a par
ailleurs un sens spécial dans le micro-langage de regexps (comme `+`, `*`, `[`
et autres ...),
   * sachant que par ailleurs le `.`  est le *wildcard* pour un seul caractère;
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



    input = "abcd"
    
    for regexp in ['abcd', 'ab[cd][cd]', r'abc.', r'abc\.']:
        print regexp, "-> \t", re.match(regexp, input)

Pour ce dernier exemple, comme on a backslashé le `.` il faut que la chaîne en
entrée contienne vraiment un `.`&nbsp;:


    print re.match (r"abc\.", "abc.")

##### En série ou en parallèle

Si je fais une analogie avec les montages électriques, jusqu'ici on a vu le
montage en série&nbsp;: on met des expressions régulières bout à bout, qui
filtrent (`match`) la chaine en entrée séquentiellement du début à la fin. On a
*un peu* de marge pour spécifier des alternatives, lorsqu'on fait par exemple

    "ab[cd]ef"

mais c'est limité à **un seul** caractère. Si on veut reconnaitre deux mots qui
n'ont pas grand-chose à voir comme `abc` **ou** `def`, il faut en quelque sorte
mettre deux regexps en parallèle, et c'est ce que permet l'opérateur `|`


    regexp = "abc|def"
    
    for input in [ 'abc', 'def', 'aef' ]:
        print input, re.match(regexp, input)

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


    input = 'abcd'
    
    for regexp in [ 'bc', r'\Aabc', '^abc', r'\Abc', '^bc', r'bcd\Z', 'bcd$', r'bc\Z', 'bc$' ]:
        print regexp, "->   \t", re.search(regexp,input)

On a en effet bien le pattern `bc` dans la chaine en entrée, mais il n'est ni au
début ni à la fin.

##### Parenthéser - (grouper)

Pour pouvoir faire des montages élaborés il faut pouvoir parenthéser&nbsp;:


    # une parenthése dans une RE pour mettre en ligne
    # un début 'a', deux possibilités pour le milieu 'bc' ou 'de' 
    # et une fin 'f'
    for input in [ 'abcf', 'adef', 'abf' ]:
        print input, re.match("a(bc|de)f", input)

##### Compter les répétitions

Vous disposez des opérateurs suivants&nbsp;:
 * `*` l'étoile qui signifie n'importe quel nombre, même nul, d'occurrences  -
par exemple, `(ab)*` pour indiquer `''` ou `'ab'` ou `'abab'` ou etc.,
 * `+` le plus qui signifie au moins une occurrence - e.g. `(ab)+` pour `ab` ou
`abab` ou `ababab` ou etc.
 * `?` qui indique une option, c'est-à-dire 0 ou 1 occurence - e.g. `(ab)?` pour
`''` ou `ab`,
 * `{n}` pour exactement n occurrences de `(ab)` - e.g. `(ab){3}` qui serait
exactement équivalent à `ababab`;
 * `{m,n}` entre m et n fois inclusivement, c'est-à-dire que `*<re>*?` est
exactement équivalent à `*<re>*{0,1}`.


    inputs = [ n*'ab'for n in [0, 1, 3, 4]] + [ 'foo' ]
    
    for regexp in [ '(ab)*', '(ab)+', '(ab){3}', '(ab){3,4}' ]:
        # on ajoute \A \Z pour matcher toute la chaine
        line_regexp = r"\A{}\Z".format(regexp)
        for input in inputs:
            print 'RE', line_regexp, '    \tINPUT', input, '->       \t', re.match(line_regexp, input)

### Greedy *vs* non-greedy

Lorsqu'on stipule une répétition un nombre indéfini de fois, il se peut qu'il
existe **plusieurs** façons de filtrer l'entrée avec l'expression régulière. Que
ce soit avec `*`, ou `+`, ou `?`, l'algorithme va toujours essayer de trouver la
**séquence la plus longue**, c'est pourquoi on qualifie l'approche de *greedy* -
quelque chose comme glouton en français&nbsp;:


    # si on cherche `<.*>` dans cette chaîne
    line='<h1>Title</h1>'
    
    # sans rien préciser
    re_greedy = '<(.*)>'
    
    # on obtient
    match = re.match(re_greedy, line)
    match.groups()


Ça n'est pas forcément ce qu'on voulait faire; aussi on peut spécifier
l'approche inverse, c'est-à-dire de trouver la **plus-petite** chaîne qui
matche, dans une approche dite *non-greedy*&nbsp;:


    # la version non-greedy a un point d'interrogation après +, * ou ?
    re_non_greedy = re_greedy = '<(.*?)>'
    
    # et cette fois, on obtient
    match = re.match(re_non_greedy, line)
    match.groups()
    


****

On peut mettre un "\n" comme caractère (et faire des RE multilignes)


    lexer + parser 
