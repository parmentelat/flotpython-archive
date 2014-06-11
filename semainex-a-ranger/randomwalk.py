#!/usr/bin/python

import random

from argparse import ArgumentParser

# our random walk does not have equal probabilities for going up or down
# this function takes in argument an integer, and returns a tuple
# (left, right) 
# this is ready for use with random.randint, meaning we will issue
# randint (left,right) and go left or right 
# whether the result is neg. or pos. respectively

# we want to make sure we remain in a constrained range
# so border is the positive threshold that we should not exceed

def left_right (n, border):
    # handle the case where n >=0
    a=abs(n)
    # if we reach the limit, bounce back
    if a >= border: 
        result = (1,2) # always positive
    # otherwise
    # we need the range to move twice as slowly as the index, so 
    # we multiply by 2
    # 0 : -b .. +b
    # 1 : -b-1 .. b-1
    # 2 : -b-2 .. b-2
    # ..
    # b-1: -2b-1 .. 1
    else:
        result = ( -border-a , border-a)
        
    # now handle the case where n < 0
    if (n<0):
        (l,r)=result
        result=(-r,-l)

    return result

class RandomWalk:
    def __init__ (self, length, border):
        self.length=length
        self.border=border
        self.counter=0
        self.current=0
    def __iter__(self):
        return self
    def next(self):
        if self.counter==self.length:
            raise StopIteration
        # return current position and compute next
        result=(self.counter, self.current)
        self.counter += 1
        # compute sign of next move
        if self.current==self.border:
            move=-1
        elif self.current== -self.border:
            move=1
        else:
            move=random.randint(-1,1)
        self.current += move
        return result
        
def main ():
    parser = ArgumentParser (description="generate a randomwalk of length <length> and with absolute value constrained by <border>")
    parser.add_argument ("length", type=int)
    parser.add_argument ("border", type=int)
    args=parser.parse_args ()

    random.seed()
    for r in RandomWalk (args.length, args.border):
        print r
    # xxx to display ...

if __name__ == '__main__':
    main()
