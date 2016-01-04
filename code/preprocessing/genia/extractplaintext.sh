#!/usr/bin/env bash

function usage {
cat << EOF
Converts GENIA Treebank XML files to plaintext and extracts gold standard sentence boundaries.

Usage: `basename $0` XMLDIR PLNDIR BOUNDSDIR

    XMLDIR     directory where Treebank XML files are stored
    PLNDIR     directory to write plaintext files to
    BOUNDSDIR  directory to write extracted sentence boundaries to
EOF
}

## Validate input
corpus=$1
plaintext=$2
bounds=$3
if [ -z $corpus ] || [ -z $plaintext ] || [ -z $bounds ]; then
    usage
    exit
fi

# print intro message
cat << EOF
Converting GENIA treebank to plaintext...
        Source data: $corpus
        Destination: $plaintext
        Bounds dir: $bounds
EOF

if [ ! -d $plaintext ]; then
    mkdir $plaintext
fi
if [ ! -d $bounds ]; then
    mkdir $bounds
fi

echo
counter=0

for f in $corpus/[0123456789]*.xml
do
    #strip newlines
    tmpf=${f}.tmp
    tr -d "\n" < $f > $tmpf
    #pull plaintext
    python plaintext.py $tmpf $plaintext/`basename $f`.txt $bounds/`basename $f`.bounds
    rm $tmpf
    counter=$(($counter + 1))
    echo -ne "\rProcessed $counter files..."
done

echo; echo Done!
