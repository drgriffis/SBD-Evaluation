#!/usr/bin/env bash

BASHRC=/home/vagrant/.bashrc
INSTALL=/vagrant/install
DATA=/vagrant/data

## Set up directories as necessary
mkdir -p $INSTALL/ctakes
mkdir -p $DATA/i2b2/plaintext

## Install necessary *nix packages
apt-get update
apt-get install -y unzip
apt-get install -y openjdk-7-jre-headless
apt-get install -y make

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
