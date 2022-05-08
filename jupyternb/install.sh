#!/bin/bash

pip install -r requirements.txt
pip uninstall -y networkx
pip install networkx
pip uninstall -y pyrender
pip install git+https://github.com/mmatl/pyrender.git
