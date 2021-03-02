#!/bin/bash

if [[ ! -f .v ]]
then
	python3 -m venv .v
fi

pip install -r requirements.txt

source .v/bin/activate

python3 main.py
