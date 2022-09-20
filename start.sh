#!/bin/bash
python manage.py migrate
echo "***** STARTING SERVER ON PORT 5000 *****"
exec gunicorn -w 4 -b 0.0.0.0:5000 mk8.wsgi:application
