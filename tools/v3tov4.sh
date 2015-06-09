#!/bin/sh

for i in $@; do
    base=$(basename $i .ipynb)
    ### do not deal with *.nbconvert.ipynb
    norm=$(basename $base .nbconvert)
    [ "$norm" != "$base" ] && continue
    ### ignore symlinks
    [ -h $i ] && echo continue
    ###
    echo "Converting $i in place"
    ipython nbconvert --to=notebook --nbformat=4 $i
    mv -f $base.nbconvert.ipynb $i
done
