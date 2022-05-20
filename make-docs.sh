#!/bin/bash

rm -rf docs/*
jupyter-book build jupyternb --path-output docs
mv docs/_build/html/* docs/
jupyter-book build jupyternb --path-output docs --builder pdflatex
mv docs/_build/latex/book.pdf docs
rm -rf docs/_build/
rm -rf docs/_sources/
