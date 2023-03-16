#!/bin/bash

python3 -m unittest
python3 setup.py sdist
python3 -m pip install dist/metrics-0.1.0.tar.gz