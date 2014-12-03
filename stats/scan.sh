#!/bin/bash

if [[ -n "$@" ]]; then
    toscan="$@"
else
    toscan=[0-9]*[0-9]
fi

for dir in $toscan; do
    [ -d $dir ] || { echo $dir not a directory - skipped; continue; }
    echo Scanning $dir
    ./scan.py $dir > $dir.scan
done
