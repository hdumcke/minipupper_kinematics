#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# we test if the MangDang python module is installed
# if it is we assume we are running on a physical minipupper
if ! (pip freeze | grep Mangdang > /dev/null)  ; then
    $BASEDIR/jupyternb/install.sh
fi
$BASEDIR/controller/install.sh
$BASEDIR/webserver/install.sh
