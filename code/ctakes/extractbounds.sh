#!/usr/bin/env bash

function usage {
cat << EOF
Extracts sentence boundaries from cTAKES output.

Usage: ./ctakesboundaries.sh XMLDIR BNDSDIR

    XMLDIR   path to directory containing cTAKES XML output
    BNDSDIR  path to write sentence bounds to
EOF
}

## validate input
xmlDir=$1
bndsDir=$2
if [ -z $xmlDir ] || [ -z $bndsDir ]; then
    usage
    exit
fi

## setup and status
if [ ! -d $bndsDir ]; then
    mkdir $bndsDir
fi
cat << EOF
Extracting sentence boundaries detected by cTAKES
  Src dir: $xmlDir
  Out dir: $bndsDir

Working...
EOF
echo

## bound extraction
gptrn="org\.apache\.ctakes\.typesystem\.type\.textspan\.Sentence"
aptrn='{print $5 "," $6}'
sptrn='s/[(begin=")|(end=")]//g'

counter=0
for f in $xmlDir/*.xml
do
    tmp=${f}.tmp
    out=$bndsDir/`basename $f`.bounds
    grep "$gptrn" $f > $tmp
    awk "$aptrn" $tmp | sed -e "$sptrn" > $out
    rm $tmp

    counter=$((counter + 1))
    echo -ne "Processed: $counter files.\r"
done

echo -e "\n\nDone!"
