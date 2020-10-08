from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from .models import Review


BIRTH_YEAR_CHOICES = range(1915, datetime.now().year)


class SignupForm(forms.Form):
    """The sign up form"""
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    def signup(self, request, user):
        """Signs up the user"""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class CustomUserChangeForm(UserChangeForm):
    """The custom user change form for the my account page"""
    password = None

    class Meta:
        """Controls the display of the custom user change form"""
        model = get_user_model()
        fields = (
            'email', 'username', 'first_name', 'last_name', 'dob',
        )
        widgets = {
            'dob': forms.SelectDateWidget(
                attrs={
                    'style': 'width: 31%; display: inline-block; margin: 0 1%'
                },
                years=BIRTH_YEAR_CHOICES
            )
        }


class ReviewForm(forms.ModelForm):
    """The review submission form"""
    class Meta:
        """Controls the display of the review submission form"""
        model = Review
        fields = ['review', 'anonymous']
        widgets = {
            'review': forms.Textarea(
                attrs={'cols': 50, 'rows': 5, 'autofocus': True,
                       'placeholder': 'Write your review!'}
            )  # cols may not do anything
        }
        labels = {
            'review': 'Leave a review!'
        }
        help_texts = {
            'anonymous': 'Check this if you don\'t want your username displayed',
        }
