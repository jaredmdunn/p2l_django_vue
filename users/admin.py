from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()
from .models import Review

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """The custom user admin"""
    model = CustomUser

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """The review admin"""
    model = Review
    list_display = ['user', 'review', 'created', 'featured']