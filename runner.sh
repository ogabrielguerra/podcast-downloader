#!/bin/bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python download_runner.py 
deactivate
rm -rf .venv