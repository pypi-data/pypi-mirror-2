#!/bin/sh
APPPATH=`dirname $0`
PYTHONPATH="$PYTHONPATH:$APPPATH" exec python2.6 $APPPATH/bin/pynagram $*
