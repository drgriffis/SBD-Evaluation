#!/usr/bin/env bash

function usage {
cat << EOF
Converts Switchboard Penn Treebank-format PRD files to plaintext and extracts gold standard sentence boundaries.

Usage: `basename $0` PRDDIR PLNDIR BOUNDSDIR

    PRDDIR     directory where Switchboard PRD files are stored
    PLNDIR     directory to write plaintext files to
    BOUNDSDIR  directory to write extracted sentence boundaries to
EOF
}


## validate input
prdDir=$1
plnDir=$2
bndsDir=$3
if [ -z $prdDir ] || [ -z $plnDir ] || [ -z $bndsDir ]; then
    usage
    exit
fi


cat << EOF
Preprocessing Switchboard texts.
  Parsed texts in: $prdDir
  Extracting plaintext to: $plnDir
  Extracting bounds to: $bndsDir

Working...

EOF

counter=0
skipcounter=0
plncounter=0
errcounter=0
for f in $(bash listswbfiles.sh $prdDir)
do
    fn=`basename $f`
    plnfname=${fn}.txt
    if [ ! -e $plnDir/$plnfname ]; then
        python plaintext.py $prdDir/$f $plnDir/$plnfname $bndsDir/${plnfname}.bounds
        result=$?
        if [ $result -eq 0 ]; then
            plncounter=$((plncounter + 1))
        else
            errcounter=$((errcounter + 1))
        fi
    else
        skipcounter=$((skipcounter + 1))
    fi
    counter=$((counter + 1))

    echo -ne "Processed: $counter\tPlaintexted: $plncounter\tSkipped: $skipcounter\tError: $errcounter\r"
done

echo; echo Done! Processed $counter total files.
