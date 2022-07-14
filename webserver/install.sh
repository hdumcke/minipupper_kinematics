#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# we test if the MangDang python module is installed
# if it is we assume we are running on a physical minipupper otherwise we use pybullet
if (pip freeze | grep Mangdang > /dev/null)  ; then
    sudo apt install -y supervisor
    sudo cp $BASEDIR/Supervisor/run_webcontroller.conf /etc/supervisor/conf.d/
    sudo cp $BASEDIR/Supervisor/run_webcontroller.sh /etc/supervisor/conf.d/
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo bash -
    sudo apt install -y nodejs
    cd $BASEDIR/frontend/minipupper/
    npm install
    sudo npm i -g @angular/cli
    echo "no" | ng build
    sudo pip uninstall -y backend
    sudo rm -rf $BASEDIR/backend/backend.egg-info
    sudo rm -rf $BASEDIR/backend/build
    sudo pip install $BASEDIR/backend
    sudo cp $BASEDIR/../mini-pupper_description/urdf/mini-pupper_fixed.urdf /etc/minipupper
else
    pip install $BASEDIR/backend
    cp $BASEDIR/../mini-pupper_description/urdf/mini-pupper_fixed.urdf $VIRTUAL_ENV/etc/minipupper
    sed -i "s|package://mini-pupper_description|.|" $VIRTUAL_ENV/etc/minipupper/mini-pupper_fixed.urdf
fi
