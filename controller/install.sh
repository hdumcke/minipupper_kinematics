#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# we test if the MangDang python module is installed
# if it is we assume we are running on a physical minipupper otherwise we use pybullet
if (pip freeze | grep Mangdang > /dev/null)  ; then
    sudo BEZIER_NO_EXTENSION=true pip install bezier --no-binary=bezier
    sudo cp -r $BASEDIR/minipupper/etc/minipupper /etc
    sudo sed -i "s|servos_dir: ../servos|servos_dir: $BASEDIR/servos|" /etc/minipupper/minipupper.yaml
    sudo sed -i "s|simulator|minipupper|" /etc/minipupper/minipupper.yaml
    sudo git config --global --add safe.directory $(echo $BASEDIR | sed "s|/controller||") # temporary fix https://bugs.launchpad.net/devstack/+bug/1968798
    sudo pip install $BASEDIR/minipupper
else
    pip install pybullet
    # we assume we are running in a virtual environment
    mkdir $VIRTUAL_ENV/etc/
    cp -r $BASEDIR/minipupper/etc/minipupper $VIRTUAL_ENV/etc/
    cp $BASEDIR/../mini-pupper_description/urdf/mini-pupper.urdf $VIRTUAL_ENV/etc/minipupper
    cp -r $BASEDIR/../mini-pupper_description/meshes $VIRTUAL_ENV/etc/minipupper
    sed -i "s|package://mini-pupper_description|.|" $VIRTUAL_ENV/etc/minipupper/mini-pupper.urdf
    sudo sed -i "s|servos_dir: ../servos|servos_dir: $BASEDIR/servos|" $VIRTUAL_ENV/etc/minipupper/minipupper.yaml
    pip install $BASEDIR/minipupper
fi
