#!/bin/bash
python manage.py migrate
echo "***** STARTING SERVER ON PORT 5000 *****"
exec python manage.py runserver 0.0.0.0:5000

