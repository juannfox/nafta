#!/bin/bash

#################################
#Launcher for Python environment#
#################################

if ! [ -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip3 install -r linters.txt
pip3 install -r requirements.txt