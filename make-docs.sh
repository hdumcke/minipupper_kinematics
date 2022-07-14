#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

rm -rf $BASEDIR/docs/*
jupyter-book build $BASEDIR/jupyternb --path-output docs
mv $BASEDIR/docs/_build/html/* $BASEDIR/docs/
jupyter-book build $BASEDIR/jupyternb --path-output docs --builder pdflatex
mv $BASEDIR/docs/_build/latex/book.pdf $BASEDIR/docs
rm -rf $BASEDIR/docs/_build/
rm -rf $BASEDIR/docs/_sources/

# set servo angles to pushup
cp $BASEDIR/controller/servos/pushup/* $BASEDIR/controller/servos/
