# Deployment checklist (add as needed)
- install Gunicorn as a WSGI server (Web Server Gateway Interface)
- install Psycopg to connect with a PostgreSQL database
- install environs for environment variables
- update DATABASES in django_project/settings.py
- install WhiteNoise for static files
- generate a requirements.txt file
- add .dockerignore file
- create .env file
- update .gitignore file
- update ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DEBUG, and SECRET_KEY

# Gunicorn
Gunicorn is a production-ready WSGI server for your project that replaces the Django local development server.

Install:
`python3 -m pip install gunicorn==20.1.0`