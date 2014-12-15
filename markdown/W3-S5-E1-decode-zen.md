
# Décoder le module `this`

## Exercice - niveau avancé

### Le module `this` et le *zen de python*

Nous avons déjà eu l'occasion de parler du *zen de python*; on peut lire ce
texte en important le module `this` comme ceci


    import this

Il suit du cours qu'une fois cet import effectué nous avons accès à une variable
`this`, de type module:


    this

### But de l'exercice

Le but de l'exercice est de deviner le contenu du module, et d'écrire une
fonction `decode_zen`, qui retourne le texte du manifeste.


    from corrections.w3_decode_zen import exo_decode_zen

### Indices

Cet exercice peut paraître un peu déconcertant; voici quelques indices
optionnels :


    dir(this)

Vous pouvez ignorer `this.c` et `this.i`, les deux autres variables du module
sont importantes pour nous.


    # le résultat attendu
    resultat = exo_decode_zen.resultat(this)

Ceci devrait vous donner une idée de comment utiliser une des deux variables du
module


    len(this.s) == len(resultat)

À quoi peut bien servir l'autre ?


    this.d[this.s[0]] == resultat[0]

Le texte comporte certes des caractères alphabétiques


    len(this.d)

mais pas seulement; les autres sont préservés.

### À vous de jouer


    def decode_zen(this):
        "<votre code>"

### Correction


    exo_decode_zen.correction(decode_zen, this)
