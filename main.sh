#!/bin/bash
export PYTHONPATH=/usr/sap/HDB/home/sap/hdbclient/
database=$1
python3 -E main.py "$database"