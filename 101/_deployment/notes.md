# Deployment checklist (add as needed)
- install Gunicorn as a WSGI server (Web Server Gateway Interface)
- generate a requirements.txt file
- update ALLOWED_HOSTS in django_project/settings.py 
- add .dockerignore file

# Gunicorn
Gunicorn is a production-ready WSGI server for your project that replaces the Django local development server.

Install:
`python3 -m pip install gunicorn==20.1.0`