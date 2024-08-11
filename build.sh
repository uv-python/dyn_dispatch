#!/usr/bin/env sh
pip3 install -r ./requirements.in
stubgen -p dyn_dispatch -o .
python3 -m build .
pip3 freeze > ./requirements.txt
