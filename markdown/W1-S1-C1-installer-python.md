
# Installer la distribution standard python

## Complément - niveau basique

Comme expliqué dans la vidéo d'introduction, vous rencontrez pour la première
fois un exemple de "notebook", dans une version simplifiée puisqu'il ne contient
aucun fragment de code pour l'instant.

Ce tout premier complément a pour but de vous donner quelques guides pour
l'installation de la distribution standard python 2.7. Ce sera la seule fois
dans le cours où nous aurons besoin de détailler des variantes selon votre
système d'exploitation.

Notez bien qu'il ne s'agit ici que d'indications, il existe de nombreuses façons
de procéder.

En cas de souci, commencez par chercher par vous-même sur google ou autre une
solution à votre problème.

Le point important est de **bien vérifier le numéro de version** de votre
installation qui doit être 2.7.*x*

# Installation de base

### Vous utilisez Windows

La méthode recommandée sur Windows est de partir de la page
https://www.python.org/download
où vous trouverez un programme d'installation qui contient tout ce dont vous
aurez besoin pour suivre le cours.

Pour vérifier que vous êtes prêts, il vous faut lancer IDLE (quelque part dans
le menu Démarrer) et vérifier le numéro de version.

### Vous utilisez MacOS

Ici encore, la méthode recommandée est de partir de la page
https://www.python.org/download
et d'utiliser le programme d'installation.

Sachez aussi, si vous utilisez déjà MacPorts (https://www.macports.org), que
vous pouvez également utiliser cet outil pour installer python 2.7 avec la
commande

    % sudo port install python27

### Vous utilisez Linux

Dans ce cas il y est très probable que python-2.7 est déjà disponible sur votre
machine. Pour vous en assurer, essayez de lancer la commande `python` dans un
terminal.

##### Redhat / Fedora

Voici par exemple ce qu'on obtient depuis un terminal sur une machine installée
en Fedora-20

    $ python
Python 2.7.5 (default, Feb 19 2014, 13:47:28)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
$

**Vérifiez bien le numéro de version** qui doit être en 2.7. Si vous obtenez un
message du style `python: command not found` utilisez `yum` pour installer le
rpm `python` comme ceci

    $ sudo yum install python

S'agissant de `idle`, l'éditeur que nous utilisons dans le cours (optionnel si
vous êtes familier avec un éditeur de texte), vérifiez sa présence comme ceci

    $ type idle
    idle is hashed (/usr/bin/idle)

Ici encore, si la commande n'est pas disponible vous pouvez l'installer avec

    $ sudo yum install python-tools

##### Debian / Ubuntu

Ici encore, python-2.7 est sans doute déja disponible. Procédez comme ci-dessus,
voici un exemple recueilli dans un terminal sur une machine installée en
Ubuntu-14.04/trusty

    $ python
Python 2.7.6 (default, Mar 22 2014, 22:59:56)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
$

Pour installer python

    $ sudo apt-get install python

Pour installer idle

    $ sudo apt-get install idle

# Installation de librairies complémentaires

Il existe un outil très pratique pour installer les librairies python, il
s'appelle `pip`, qui est documenté ici https://pypi.python.org/pypi/pip

Sachez aussi, si par ailleurs vous utilisez un gestionnaire de package comme
`rpm` sur RedHat, `apt-get` sur debian, ou `port` sur MacOS, que de nombreux
packages sont également disponibles au travers de ces outils.
