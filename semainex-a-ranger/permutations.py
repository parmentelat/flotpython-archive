#!/usr/bin/env python

import math

class Permutations:
    def __init__ (self, n):
        self.n=n
        self.counter=0
        if n>=2:
            self.subiterator=Permutations(n-1)

    def __iter__ (self): return self

    def next (self):
        if self.n==1:
            if self.counter==0: 
                self.counter +=1
                return [1]
            else:
                raise StopIteration
        # get one <n-1> permutation if we're at the beginning of a sequence
        if self.counter==0:
            try:
                self.subsequence = self.subiterator.next()
            except:
                raise StopIteration
        # inserting <n> in the middle of a <n-1> permutation 
        # this first naive version would first issue [n n-1 .. 1]
        #result = self.subsequence[0:self.counter] + [ self.n ] + self.subsequence [ self.counter:self.n-1]
        cutter=self.n-1-self.counter
        result = self.subsequence[0:cutter] + [ self.n ] + self.subsequence [ cutter:self.n-1]
        # move the next insertion one step right, or rewind
        self.counter = (self.counter+1)%self.n
        return result

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
