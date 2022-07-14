#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pip install -r $BASEDIR/requirements.txt
pip uninstall -y networkx
pip install networkx
pip uninstall -y pyrender
pip install git+https://github.com/mmatl/pyrender.git
