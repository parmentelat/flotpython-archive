
# Itérateurs

## Complément - niveau avancé

Dans ce complément nous allons&nbsp;:
 * tout d'abord voir un autre exemple d'itérateurs, et implémenter notre propre
itérateurs des permutations d'un ensemble fini,
 * et dire quelques mots du module `itertools` qui fournit des itérateurs
communs, comme par exemple, justement, les permutations, les combinaisons, et
autres outils combinatoires usuels.

### Les permutations

##### C'est quoi déjà les permutations ?

En guise de rappel, l'ensemble des permutations d'un ensemble fini correspond à
toutes les façons d'ordonner ses éléments; si l'ensemble est de cardinal $n$ il
possède $n!$ permutations, on a $n$ façons de choisir le premier élément, $n-1$
façons de choisir le second, etc.

Comme on vient de le dire, un itérateur sur les permutations est disponible au
travers du module standard `itertools`. Cependant il nous a semblé intéressant
de vous montrer comment on pourrait écrire nous-mêmes cette fonctionnalité, de
manière relativement simple.

Pour illustrer le concept, à quoi ressemblent les 6 permutations d'un ensemble à
trois éléments&nbsp;:


    from itertools import permutations


    set = {1,2,3}
    
    for p in permutations (set):
        print p

##### Une implémentation 

Voici une implémentation possible pour un itérateur de permutations&nbsp;:


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
            # on insère alors n-1 (car les indices commencent à 0)
            # successivement dans la sous-sequence à l'indice counter
            #
            # naivement on écrirait
            # result = self.subsequence[0:self.counter] + [ self.n - 1 ] \
            #    + self.subsequence [self.counter:self.n-1]
            # mais ça revient à mettre le nombre le plus élevé en premier
            # et donc à itérer les permutations dans le mauvais ordre,
            # en commençant par la fin
            #
            # donc on fait plutôt une symétrie
            # pour insérer en commençant par la fin
            cutter = self.n-1 - self.counter
            result = self.subsequence[0:cutter] + [ self.n - 1 ] \
                     + self.subsequence[cutter:self.n-1]
            # 
            # on n'oublie pas de maintenir le compteur et de
            # le remettre à zéro tous les n tours
            self.counter = (self.counter+1) % self.n
            return result
    
        # la longeur de cet itérateur est connue
        def __len__ (self):
            return math.factorial(self.n)
