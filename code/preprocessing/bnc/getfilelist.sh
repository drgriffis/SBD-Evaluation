#!/usr/bin/env bash

function usage {
cat << EOF
Generates a list of relative paths to all BNC XML files from the input XML root.

Usage: `basename $0` XMLDIR OUTFILE

    XMLDIR   path to root directory of BNC XML files
    OUTFILE  file to write list of relative paths to
EOF
}


## Validate input
xmldir=$1
outf=$2
if [ -z $xmldir ] || [ -z $outf ]; then
    usage
    exit
fi

## Generate the file list
ls -R $xmldir > $outf

# fill in relative paths from $xmldir root
tmpf=${outf}.tmp
root=`echo $xmldir | awk -F '/' '{ print $2 }'`
awk -F "/" '
{
    if (match($0, /^\/'$root'\//)) {
        curdir = $(NF-1) "/" $(NF)
    } else if (match($0, /.*.xml$/)) {
        print curdir "/" $1
    }
}
' $outf > $tmpf

# remove extraneous colon character
sed -e 's/://' $tmpf > $outf
rm $tmpf
