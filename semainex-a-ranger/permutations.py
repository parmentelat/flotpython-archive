#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import math

class Permutations:
    """
    Un itérateur qui énumère les permutations de n
    sous la forme d'une liste d'indices commençant à 0
    """
    def __init__ (self, n):
        # le constructeur bien sûr ne fait (presque) rien
        self.n=n
        # le compteur va aller de 0 à n-1
        # puis comme ça en boucle sans fin
        self.counter=0
        # on se contente d'allouer un iterateur de rang n-1
        # si bien qu'une fois qu'on a fini de construire
        # l'objet d'ordre n on a n objets Permutations en tout
        if n>=2:
            self.subiterator=Permutations(n-1)

    # pour satisfaire le protocole de l'iterable
    def __iter__ (self):
        return self

    # c'est ici bien sûr que se fait tout le travail
    def next (self):

        # pour n ==1
        # le travail est très simple
        if self.n==1:
            # on doit renvoyer une fois la liste [0]
            # car les indices commencent à 0
            if self.counter==0: 
                self.counter +=1
                return [0]
            # et ensuite c'est terminé
            else:
                raise StopIteration

        # pour n >= 2
        # lorsque counter est nul,
        # on traite la permutation d'ordre n-1 suivante 
        if self.counter==0:
            self.subsequence = self.subiterator.next()
        #
        # dans laquelle
        # on va insérer n 
        # à n places différentes
        # on insère alors n (en fait n-1 car les indices commencent à 0)
        # successivement dans la sous-sequence à l'indice counter
        #
        # naivement on ecrirait
        # result = self.subsequence[0:self.counter] + [ self.n - 1 ] + self.subsequence [self.counter:self.n-1]
        # mais ça revient à mettre le nombre le plus élevé en premier
        # et donc à itérer les permutations dans le mauvais ordre,
        # en commençant par la fin
        #
        # donc on fait plutôt une symétrie
        # pour insérer en commençant par la fin
        cutter = self.n-1 - self.counter
        result = self.subsequence[0:cutter] + [ self.n - 1 ] + self.subsequence[cutter:self.n-1]
        # 
        # on n'oublie pas de maintenir le compteur et de le remettre à zéro
        # tous les n tours
        self.counter = (self.counter+1) % self.n
        return result

    # la longeur de cet itérateur est connue
    def __len__ (self):
        return math.factorial(self.n)


# show the <max> first permutations - or all of them if max is None or False
def show_first_permutations  (n,max=None):
    iterator = Permutations (n)
    print "Il y a ",len(iterator),"permutations d'ordre",n
    counter=0
    for s in iterator:
        print s
        counter+=1
        if max and counter>=max:
            print '....'
            break

from argparse import ArgumentParser

def main ():
    parser=ArgumentParser()
    parser.add_argument("-f","--first",dest='max',default=None,type=int,help="list only the <N> first permutations")
    parser.add_argument("n",type=int)
    args=parser.parse_args()
    show_first_permutations (args.n, args.max)

if __name__ == '__main__':
    main()
