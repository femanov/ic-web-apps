#!/bin/sh

python3 manage.py makemigrations
python3 manage.py makemigrations accdb
python3 manage.py makemigrations netdb


python3 manage.py migrate
python3 manage.py migrate --database=icdata
python3 manage.py migrate --database=netdata
