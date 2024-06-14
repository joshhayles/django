from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.mailchimp_add_member import add_member_to_mailchimp

# AbstractUser (which subclasses AbstractBaseUser) is the recommended approach vs AbstractBaseUser because it's easier to update additional fields

class CustomUser(AbstractUser):
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=5, blank=True)
    
    # null is database-related. When it is set to True, it can store a dabase entry as NULL
    # blank is validation-related. If this is True, a form will allow an empty value vs a value being required

@receiver(post_save, sender=CustomUser)
def add_user_to_mailchimp(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        first_name = instance.first_name
        last_name = instance.last_name
        address = {
            "addr1": instance.address,
            "city": instance.city,
            "state": instance.state,
            "zip": instance.zip,
        }
        # Retrieve address details from the user's profile or registration form if available
        # and populate the `address` dictionary accordingly
        add_member_to_mailchimp(email, first_name, last_name, address)
