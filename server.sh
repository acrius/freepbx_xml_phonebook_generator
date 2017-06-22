#!/bin/bash

DEVDIR=/home/admindok/dev/freepbx_xml_phonebook_generator 
VENVDIR=$DEVDIR/env

cd $DEVDIR
source $VENVDIR/bin/activate
python3 server.py
