#!/bin/sh

python3 manage.py makemigrations accdb
python3 manage.py migrate --database=icdata
