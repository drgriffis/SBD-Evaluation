#!/bin/bash

srcd=/vagrant/data/i2b2/plaintext
outd=/vagrant/data/i2b2/splitta-output
splitta=/vagrant/install/splitta/splitta.1.03/sbd.py
svmmodel=/vagrant/install/splitta/splitta.1.03/model_svm
nbmodel=/vagrant/install/splitta/splitta.1.03/model_nb
model=
shortmodel=
while getopts "m:" OPTION; do
    case $OPTION in
        m)
            if [ "$OPTARG" = "svm" ]; then
                model=$svmmodel
            elif [ "$OPTARG" = "nb" ]; then
                model=$nbmodel
            fi
            shortmodel=$OPTARG
            ;;
    esac
done

usage() {
cat << EOF
Usage: `basename $0` -m [svm/bn]
EOF
}
if [ -z $model ]; then
    usage
    exit
fi

outd=$outd/$shortmodel
bounds=$outd/bounds
if [ ! -d $outd ]; then
    mkdir -p $outd
fi
if [ ! -d $bounds ]; then
    mkdir -p $bounds
fi

cat << EOF
Running SPLITTA parser to find sentence boundaries on i2b2 corpus
  Src data: $srcd
  Output to: $outd
  Bounds to: $bounds
  
Working...
EOF

counter=0
processed=0
skipped=0
error=0
for f in $srcd/*.txt
do
    python $splitta -m $model -o $outd/`basename $f`.sentences -b $bounds/`basename $f`.bounds $f 2>/dev/null
    if [ $? -eq 0 ]; then
        processed=$((processed + 1))
    else
        error=$((error + 1))
    fi
    counter=$((counter + 1))

    echo -ne "                                                              \rSeen: $counter\tExtracted: $processed\tError: $error\r"
done

echo; echo Done! Processed $counter files in total.
