import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
superuser = User.objects.filter(is_superuser=True).first()

print(f"Superuser exists: {superuser is not None}")
if superuser:
    print(f"Username: {superuser.username}")
else:
    print("No superuser found")

#tinywall4