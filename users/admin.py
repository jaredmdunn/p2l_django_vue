from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()
from .models import Review

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review