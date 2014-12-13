#!/bin/bash
#
# to be used in conjunction with
#  	recode     ISO-8859-15..UTF-8     $file
#
#

for file in "$@"; do
    # is there a coding line already ?
    grep -q 'coding: utf-8' $file && {
	echo "coding utf-8 already present in $file - skipped"
	continue;
    }
    grep -q 'coding:' $file && {
	echo "WARNING $file has some other coding line - REQUIRES MANUAL ACTION"
	continue;
    }
    
    ed $file > /dev/null 2>&1 <<EOF
1
i
# -*- coding: utf-8 -*-
.
wq
EOF
    echo "Added a coding: utf-8 line to $file"
    done
