#!/bin/bash

url=https://profs:ENSelearn1ng@course-41001.france-universite-numerique-mooc.fr/corrections/corrections.tar.gz

date=$(date +%m-%d)

[ -d ${date} ] && mv ${date} ${date}.bak

[ -d "students" ] && { echo "found an existing students dir - exiting"; exit; }

curl -o corrections-${date}.tar.gz ${url}

tar xvfz corrections-${date}.tar.gz

mv -f students ${date}



