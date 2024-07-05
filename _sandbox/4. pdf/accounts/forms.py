from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip",
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip",
        )