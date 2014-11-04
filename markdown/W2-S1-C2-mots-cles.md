
# Les mots-clés de python

### Mots réservés

Il existe en python certains mots spéciaux, qu'on appelle des mots-clés, ou
`keywords` en anglais, qui sont réservés et **ne peuvent pas être utilisés**
comme identifiants, c'est-à-dire comme un nom de variable.

C'est le cas par exemple pour l'instruction `print`, que nous verrons
prochainement, et qui comme son nom l'indique imprime un résultat


    print "Hello world !"

À cause de la présence de cette instruction dans le langage, il n'est pas
autorisé d'appeler une variable `print`:


    # interdit
    print = 1

### Liste complète

Voici la liste complète des mots-clés:

<table border="0"><tbody>
<tr><td>`and`</td>       <td>`del`</td>       <td>`from`</td>
<td>`not`</td>       <td>`while`</td></tr>
<tr><td>`as`</td>        <td>`elif`</td>      <td>`global`</td>    <td>`or`</td>
<td>`with`</td></tr>
<tr><td>`assert`</td>    <td>`else`</td>      <td>`if`</td>
<td>`pass`</td>      <td>`yield`</td></tr>
<tr><td>`break`</td>     <td>`except`</td>    <td>`import`</td>
<td>`print`</td> <td></td> </tr>
<tr><td>`class`</td>     <td>`exec`</td>      <td>`in`</td>
<td>`raise`</td> <td></td> </tr>
<tr><td>`continue`</td>  <td>`finally`</td>   <td>`is`</td>
<td>`return`</td> <td></td> </tr>
<tr><td>`def`</td>       <td>`for`</td>       <td>`lambda`</td>
<td>`try`</td> <td></td> </tr>
</tbody></table>

Il vous faudra donc y prêter attention, surtout au début; avec un tout petit peu
d'habitude vous saurez rapidement les éviter. Vous remarquerez aussi que tous
les bons éditeurs de texte supportant du code Python vont colorer les mots-clès
différemment des variables. Par exemple, IDLE colorie les mots-clès en orange,
vous pouvez donc très facilement vous rendre compte que vous allez, par erreur,
en utiliser un comme nom de variable. On appelle cette fonctionalité la
coloration syntaxique, et elle permet d'identifier facilement (grâce à un code
de couleur) le rôle de différents éléments de votre code (variable, mots-clès,
etc.) D'une manière générale, nous vous déconseillons fortement d'utiliser un
éditeur de texte qui n'offre pas cette fonctionalité de coloration syntaxique.
En particulier, IDLE, emacs et eclipse offrent un support approprié, incluant la
coloration syntaxique, pour programmer en Python.

### Pour en savoir plus

On peut se reporter à cette page

https://docs.python.org/2/reference/lexical_analysis.html#keywords
