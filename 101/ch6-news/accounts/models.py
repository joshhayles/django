from django.db import models
from django.contrib.auth.models import AbstractUser
# AbstractUser (which subclasses AbstractBaseUser) is the recommended approach vs AbstractBaseUser because it's easier to update additional fields

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    # null is database-related. When it is set to True, it can store a dabase entry as NULL
    # blank is validation-related. If this is True, a form will allow an empty value vs a value being required
