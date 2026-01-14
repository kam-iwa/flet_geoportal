# Flet Geoportal
Simple full-stack geoportal web app written in Python: front-end with using Flet framework, back-end with using FastAPI framework and PostgreSQL + PostGIS database

## How to run?
To run Flet Geoportal, you need just to input into terminal command `python manage.py 'parameter' '-e` or `--env-file` (optional). List of available parameters with description of each parameter:
- `up` - runs the Docker containers of API
- `build` - builds Docker containers of API
- `restart` - restarts Docker containers of API
- `down` - shuts down Docker container of API

Using this command with the additional -e or --env-file parameter and providing a .env.[filename] file will start the containers with environment variable values loaded from the specified file.