#!/bin/sh

python3 manage.py migrate --fake accdb zero
python3 manage.py migrate --fake netdb zero

find ./accdb -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ./netdb -path "*/migrations/*.py" -not -name "__init__.py" -delete


python3 manage.py makemigrations accdb
python3 manage.py makemigrations netdb


python3 manage.py migrate --database=icdata --fake-initial
python3 manage.py migrate --database=netdata --fake-initial
