#!/bin/bash

if [[ -n "$@" ]]; then
    toscan="$@"
else
    toscan=[0-9]*
fi

for dir in $toscan; do
  ./scan.py $dir > $dir.scan
done
