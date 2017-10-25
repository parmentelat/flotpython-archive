#!/bin/bash
#
# run at toplevel
#
# purpose it to refresh the mapping exercice -> week x sequence
# so that corriges.py can output stuff properly
#

while true; do
    [ -d w1 ] && break || cd .. 
    [ $(pwd) == "/" ] && { echo Cannot spot w1! ; exit 1; }
done

dst=corriges/exomap

echo "Running $0 in $(pwd) - output in $dst"

grep exo_ w?/w*-x*nb | grep import | grep from > $dst
