#!/bin/bash
# Count migrations that we still have to apply
DBFOLDER="data"
DBPATH="db.sqlite3"

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
echo "***** STARTING SERVER ON PORT 5000 *****"
exec python manage.py runserver 0.0.0.0:5000
