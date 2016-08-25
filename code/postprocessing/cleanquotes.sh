#!/bin/bash
for f in $1/*.${2}; do
    tr -d "\"" < $f > $3/`basename $f`
done
