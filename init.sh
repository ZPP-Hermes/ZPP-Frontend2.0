#!/bin/bash
virtualenv --no-site-packages --distribute .env
source .env/bin/activate
pip install -r requirements.txt
cd django_site_main
Rscript install.R
rm -f *.sqlite3
python manage.py syncdb
python manage.py loaddata datas.json
