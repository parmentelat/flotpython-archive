
# Fichiers

## Exercice - niveau basique

### Calcul du nombre de lignes, de mots et de caractères

On se propose d'écrire une * moulinette* qui annote un fichier avec des nombres
de lignes, de mots et de caractères.

Le but de l'exercice est d'écrire une fonction `comptage`:
 * qui prenne en argument un nom de fichier d'entrée (on suppose qu'il existe)
et un nom de fichier de sortie (on suppose qu'on a le droit de l'écrire);
 * le fichier d'entrée est laissé intact;
 *  pour chaque ligne en entrée, le fichier de sortie comporte une ligne qui
donne le numéro de ligne, le nombre de mots (**séparés par des espaces**), le
nombre de caractères (y compris la fin de ligne), et la ligne d'origine;
 * et enfin le fichier de sortie comporte une dernière ligne avec les nombres
totaux de lignes, de mots et de caractères, **suivi d'une dernière fin de
ligne**.

Dans sa version simple, cet exercice ne s'occupe que de **fichiers sans
caractères accentués**.


    # un exemple de ce qui est attendu
    from corrections.w4_files import exo_comptage
    exo_comptage.exemple()


    # votre code
    def comptage(in_filename, out_filename):
    #    print 'in',in_filename
    #    print 'out',out_filename
        "<votre_code>"


    # pour vérifier votre code
    exo_comptage.correction(comptage)

La méthode `debug` applique votre fonction au premier fichier d'entrée, et
affiche le résultat comme dans l'exemple ci-dessus.

**N'oubliez pas de vérifier** que vous ajoutez bien la dernière fin de ligne,
car sa présence/absence n'apparaît pas clairement dans ce tableau.


    # debugging
    exo_comptage.debug(comptage)

### Accès aux fichiers d'exemples

Vous pouvez télécharger les fichiers d'exemples&nbsp;:
 * [Romeo and Juliet](data/romeo_and_juliet.txt)
 * [Lorem Ipsum](data/lorem_ipsum.txt)

Ainsi que pour les courageux, des fichiers avec accents&nbsp;:
 * [Une charogne en Unicode](une_charogne_unicode.txt)
 * [Une charogne en Iso-latin-15](une_charogne_iso15.txt)

À nouveau ces deux fichiers ne sont pas à prendre en compte dans la version
basique de l'exercice.
