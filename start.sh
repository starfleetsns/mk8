#!/bin/bash
set -ex
# Count migrations that we still have to apply
DBFOLDER="data"
DBPATH="db.sqlite3"

CREATESUPERUSER=$(cat <<EOF
from os import environ
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser("admin", environ.get("ADMIN_EMAIL"), environ.get("ADMIN_PASSWORD")) if len(User.objects.filter(username="admin").all()) == 0 else print("ADMIN ALREADY THERE")

EOF
	       )

MIGRATIONS=$(python manage.py showmigrations --list | grep '\[ \]' | wc -l)
if [ "$MIGRATIONS" != "0" ]; then
    echo "***** BACKING UP DATABASE PRIOR TO MIGRATIONS *****"
    if [ -e "$DBFOLDER/$DBPATH" ]; then
	NOW=$(date +"%Y-%m-%d-%H%M%S")
	mkdir -p "$DBFOLDER/backups/"
	cp "$DBFOLDER/$DBPATH" "$DBFOLDER/backups/$NOW.sqlite3"
    fi
    python manage.py migrate
fi
echo "***** CREATING SUPERUSER IF IT DOESN'T EXIST *****"
python manage.py shell <<< "$CREATESUPERUSER"
echo "***** STARTING SERVER ON PORT 5000 *****"
exec python manage.py runserver 0.0.0.0:5000
