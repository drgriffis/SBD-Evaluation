function usage {
cat << EOF
Usage: `basename $0` PRDDIR

    PRDDIR  path to root directory of Switchboard parsed PRD files
EOF
}

prddir=$1
if [ -z $prddir ]; then
    usage
    exit
fi

root=`echo $prddir | awk -F '/' '{ print $2 }'`
ls -R $prddir | \
awk -F '/' '
{
    if (match($0, /^\/'$root'\//)) {
        curdir = $(NF)
    } else if (match($0, /.*.prd$/)) {
        print curdir "/" $1
    }
}
' | \
sed -e 's/://'
