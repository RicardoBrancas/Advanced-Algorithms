#!/bin/sh

find . -type f -iname "*.bm" -print0 | while IFS= read -r -d $'\0' line; do
    /usr/bin/time ./bipartite_match.py < $line
done
