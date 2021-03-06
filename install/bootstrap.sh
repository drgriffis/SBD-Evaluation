#!/usr/bin/env bash

BASHRC=/home/vagrant/.bashrc
INSTALL=/vagrant/install
DATA=/vagrant/data

## Set up directories as necessary
mkdir -p $INSTALL/ctakes
mkdir -p $INSTALL/splitta/svm_light
mkdir -p $DATA/i2b2/plaintext
mkdir -p $DATA/i2b2/bounds
mkdir -p $DATA/genia/plaintext
mkdir -p $DATA/genia/bounds
mkdir -p $DATA/bnc/plaintext
mkdir -p $DATA/bnc/bounds
mkdir -p $DATA/swb/plaintext
mkdir -p $DATA/swb/bounds
mkdir -p $DATA/analysis/ending-chars
mkdir -p $DATA/results

## Install necessary *nix packages
apt-get update
apt-get purge -y openjdk-6-jre-headless openjdk-6-jre-lib
apt-get install -y unzip
apt-get install -y openjdk-7-jdk
apt-get install -y make
apt-get install -y patch

## Install Java 8 (for Stanford CoreNLP)
cd /opt
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u45-b14/jdk-8u45-linux-x64.tar.gz"
tar -xzf jdk-8u45-linux-x64.tar.gz
echo "export JAVA8_HOME=/opt/jdk1.8.0_45" >> $BASHRC

## Install NLTK (for Switchboard parsing)
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
easy_install pip
pip install -U nltk

## Install ctakes
CTAKESNAME="apache-ctakes-3.2.2"
CTAKESPKG="$CTAKESNAME-bin.tar.gz"
CTAKESURL="http://apache.cs.utah.edu/ctakes/ctakes-3.2.2/$CTAKESPKG"
CTAKESRESPKG="ctakes-resources-3.2.1.1-bin.zip"
CTAKESRESURL="http://sourceforge.net/projects/ctakesresources/files/$CTAKESRESPKG"

cd $INSTALL/ctakes
if [ ! -e "$CTAKESPKG" ]; then
    wget "$CTAKESURL"
fi
if [ ! -e "$CTAKESRESPKG" ]; then
    wget "$CTAKESRESURL"
fi

if [ ! -d "$CTAKESNAME" ]; then
    tar -xzf $CTAKESPKG
fi
if [ ! -d "resources" ]; then
    unzip -q $CTAKESRESPKG
fi
cp -R resources/* $CTAKESNAME/resources/
echo "export CTAKES_HOME=`pwd`/$CTAKESNAME" >> $BASHRC

## Install Splitta
# (dependency: SVM_Light)
SVMLIGHTPKG=svm_light_linux64.tar.gz
SVMLIGHTURL="http://download.joachims.org/svm_light/current/$SVMLIGHTPKG"
cd $INSTALL/splitta/svm_light
if [ ! -e $SVMLIGHTPKG ]; then
    wget $SVMLIGHTURL
fi
tar -xzf $SVMLIGHTPKG
# (actual Splitta)
SPLITTANAME=splitta.1.03
SPLITTAPKG=splitta.1.03.tgz
SPLITTAURL="https://splitta.googlecode.com/files/$SPLITTAPKG"
cd $INSTALL/splitta
if [ ! -e $SPLITTAPKG ]; then
    wget $SPLITTAURL
fi
mkdir -p $SPLITTANAME
cp $SPLITTAPKG $SPLITTANAME/
cd $SPLITTANAME/
tar -xzf $SPLITTAPKG
rm $SPLITTAPKG
cd ../
# apply patch with code changes for SBD
patch $SPLITTANAME/sbd.py < ${SPLITTANAME}.patch

## Install Stanford-CoreNLP
SFRDNAME=stanford-corenlp-full-2015-04-20
SFRDPKG=$SFRDNAME.zip
SFRDURL="http://nlp.stanford.edu/software/$SFRDPKG"
cd $INSTALL/stanford-corenlp
if [ ! -e $SFRDPKG ]; then
    wget $SFRDURL
fi
if [ ! -d $SFRDNAME ]; then
    unzip $SFRDPKG
fi
# Stanford parser
SFRDPNAME=stanford-parser-full-2015-04-20
SFRDPPKG=$SFRDPNAME.zip
SFRDPURL="http://nlp.stanford.edu/software/$SFRDPPKG"
if [ ! -e $SFRDPPKG ]; then
    wget $SFRDPURL
fi
if [ ! -d $SFRDPNAME ]; then
    unzip $SFRDPPKG
fi

## ---
## No installation for Lingpipe, since it can't be downloaded via wget
## ---

## Download GENIA
GENIANAME="GENIA_treebank_v1"
GENIAURL="http://www.nactem.ac.uk/GENIA/current/GENIA-corpus/Treebank/$GENIANAME.tar.gz"

if [ ! -e "$DATA/genia/${GENIANAME}.tar.gz" ]; then
    cd $DATA/genia
    wget $GENIAURL
fi
