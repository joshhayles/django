from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    mdoel = CustomUser
    list_display = [
        "first_name",
        "last_name",
        "email",
        "username",
        "is_staff",
    ]

admin.site.register(CustomUser, CustomUserAdmin)
