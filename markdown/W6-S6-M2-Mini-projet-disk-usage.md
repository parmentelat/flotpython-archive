
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

### Exemple d'utilisation
