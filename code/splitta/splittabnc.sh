#!/bin/bash

srcd=/vagrant/data/bnc/plaintext
outd=/vagrant/data/bnc/splitta-output
splitta=/vagrant/install/splitta/splitta.1.03/sbd.py
svmmodel=/vagrant/install/splitta/splitta.1.03/model_svm
nbmodel=/vagrant/install/splitta/splitta.1.03/model_nb
fixer=/vagrant/code/splitta/fixsplittabnc.py
model=
shortmodel=
errfls=error.files
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
fixedbounds=$bounds/fixed
if [ ! -d $outd ]; then
    mkdir -p $outd
fi
if [ ! -d $bounds ]; then
    mkdir -p $bounds
fi
if [ ! -d $fixedbounds ]; then
    mkdir -p $fixedbounds
fi

cat << EOF
Running SPLITTA parser to find sentence boundaries on GENIA corpus
  Src data: $srcd
  Output to: $outd
  Unadjusted bounds to: $bounds
  Adjusted bounds to: $fixedbounds
  
Working...
EOF

rm $errfls

counter=0
processed=0
skipped=0
error=0
for f in $srcd/*.xml.txt
do
    prepped=$outd/`basename $f`.prepped
    slices=$outd/`basename $f`.slices
    sentences=$outd/`basename $f`.sentences
    boundsf=$bounds/`basename $f`.bounds
    adjustedbounds=$fixedbounds/`basename $f`.bounds.fixed
    # get the slices
    python $fixer -t pre -f $f -o $prepped -s $slices
    if [ $? -eq 0 ]; then
        # run splitta ON THE ORIGINAL TEXT
        python $splitta -m $model -o $sentences -b $boundsf $f 2>/dev/null
        if [ $? -eq 0 ]; then
            # and fix the slices
            python $fixer -t post -f $boundsf -s $slices -o $adjustedbounds
            if [ $? -eq 0 ]; then
                processed=$((processed + 1))
            else
                error=$((error + 1))
                echo $f >> $errfls
            fi
        else
            error=$((error + 1))
            echo $f >> $errfls
        fi
    else
        error=$((error + 1))
        echo $f >> $errfls
    fi
    counter=$((counter + 1))

    echo -ne "                                                              \rSeen: $counter\tExtracted: $processed\tError: $error\r"
done

echo; echo Done! Processed $counter files in total.
if [ $error -gt 0 ]; then
    echo List of error files in $errfls
fi
