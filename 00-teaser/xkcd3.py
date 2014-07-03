#!/usr/bin/env python

import random

import matplotlib
matplotlib.use('TkAgg')

from matplotlib import pyplot as plt
#import numpy as np

plt.xkcd()

import this
print '========================================'
def decode_c (c): return this.d[c] if c in this.d else c
def decode_l (l): return ''.join( [ decode_c(c) for c in l ])
aphorisms = [ decode_l(l) for l in this.s.split('\n') if l ]    

n=len(aphorisms)

dpi=100
# target size
x,y= 750, 400
# however we build something larger
fact=2
fig = plt.figure(dpi=dpi,figsize=(fact*float(x)/dpi,fact*float(y)/dpi))

## random but reproducible
random.seed(0)
#
X_MIN,X_MAX = 0,1.
Y_MIN,Y_MAX = 0.2,0.8
ANGLE_MIN,ANGLE_MAX = -60,60
FONT_MIN,FONT_MAX=16,32
X = [ random.uniform(X_MIN,X_MAX) for a in aphorisms ]
Y = [ random.uniform(Y_MIN,Y_MAX) for a in aphorisms ]
angles = [ random.uniform(ANGLE_MIN,ANGLE_MAX) for a in aphorisms ]
font_sizes = [ int (random.uniform(FONT_MIN,FONT_MAX)) for a in aphorisms ]
for i,a,x,y,angle,size in zip (range(n),aphorisms,X,Y,angles,font_sizes):
    pass
#    fig.text (x,y,"%s:%s"%(i,a),rotation=angle,fontsize=size,ha='center',va='center')


aphorisms = [ a.strip('.') for a in aphorisms if len(a)<=40 and 'Although' not in a ]
n=len(aphorisms)

layout = [
    (0.5,0.9,0,1.,'k','center','center'),
    (0.2,0.4,45,.8,'r','center','center'),
    (0.225,0.545,-45,.6,'b','center','center'),
    (.5,.5,0,.6,'g','center','center'),
#    (.5,.5,0,.6,'g')
]

def draw (layout):
    p=len(layout)
    for i,a,(x,y,angle,weight,color,ha,va) in zip (range(p),aphorisms[:p],layout):
        fontsize=FONT_MIN+weight*(FONT_MAX-FONT_MIN)
#        text = "%s:%s"%(i,a) if i==p-1 else a
        text = a
        fig.text (x,y,text,rotation=angle,fontsize=fontsize,color=color,ha=ha,va=va)

Y_bottom=0.08
X_bottom=0.01
X_top=0.63
delta=float(X_top-X_bottom)/(n-1)
X_current=X_bottom
ANGLE=45

layout2 = [ (X_bottom+i*delta,Y_bottom, ANGLE, .8, 'b','left','bottom')
           for i,a in zip(range(n),aphorisms) ]
layout2[0]= (0.5,0.9,0,1.4,'k','center','center')


draw (layout2)  

fig.savefig('xkcd3.png')
fig.savefig('xkcd3-750x400.png')

plt.show()
