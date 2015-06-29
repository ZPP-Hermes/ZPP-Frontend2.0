#!/bin/bash
source .env/bin/activate
cd django_site_main
pkill -f Rserve
Rscript start.R
python manage.py runserver 0.0.0.0:8000
