#!/usr/bin/env python

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
        result = self.subsequence[0:self.counter] + [ self.n ] + self.subsequence [ self.counter:self.n-1]
        # move the next insertion one step right, or rewind
        self.counter = (self.counter+1)%self.n
        return result

from argparse import ArgumentParser

def main ():
    parser=ArgumentParser()
    parser.add_argument("-f","--first",dest='max',default=None,type=int,help="list only the <N> first permutations")
    parser.add_argument("n",type=int)
    args=parser.parse_args()
    counter=0
    for s in Permutations (args.n):
        print s
        counter+=1
        if args.max and counter>=args.max:
            print '....'
            break

if __name__ == '__main__':
    main()


        
        
