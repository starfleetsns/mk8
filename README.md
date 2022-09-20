# Mario Kart 8 Championship Website
This repository contains the website to run a Mario Kart 8 tournament.

## Quick Start
```bash
# Build the container with all its dependencies
docker build -t mk8 .
# Test that the container works as intended
docker run -p 5000:5000 --rm mk8
# Check on http://localhost:5000/ that the site works correctly
```

## TODO
1. Document how to set up Google OAuth
2. Provide mounts for db.sqlite3 and media folder
3. Provide a kubernetes deployment
