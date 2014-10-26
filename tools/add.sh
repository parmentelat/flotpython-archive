#!bin/bash

name=$1; shift
seqcomp=$1; shift

name=$(basename $name .ipynb)

simple=$name.ipynb
qualified=$seqcomp-$name.ipynb

ln -s $simple $qualified
git add $simple $qualified


