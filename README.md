# Mario Kart 8 Championship Website
This repository contains the website to run a Mario Kart 8 tournament.

## Quick Start
### Development
Since the website is built with an old version of python, it requires that you have conda installed.
```bash
conda env create -p ./venv --file environment.yml
conda activate ./venv
python manage.py migrate
python manage.py runserver 5000
```

### Deployment
```bash
# Build the container with all its dependencies
docker build -t mk8 .
# Test that the container works as intended
docker run -p 5000:5000 --rm mk8
# Check on http://localhost:5000/ that the site works correctly
# Be aware that in this way the data is saved only inside the container
```

## TODO
1. Document how to set up Google OAuth
2. Add docker-compose file with volumes
3. Provide mounts for db.sqlite3 and media folder
4. Provide a kubernetes deployment
