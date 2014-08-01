# -*- coding: iso-8859-15 -*-

def multi_tri (listes):
    "trie toutes les sous-listes"
    for liste in listes:
        liste.sort()
    return listes

def multi_tri_reverse (listes, reverses):
    """tries toutes les sous listes, dans une direction
    precisee par le second argument"""
    for liste, reverse in zip(listes, reverses):
        liste.sort(reverse=reverse)
    return listes

def produit_scalaire (X,Y):
    """retourne le produit scalaire de deux listes de même taille"""
    # la dimension
    n = len(X)
    # initialisation du resultat
    scalaire = 0
    # on calcule la somme de tous les xi*yi
    for i in range (n):
        scalaire += X[i] * Y[i]
    # ne pas oublier
    return scalaire

