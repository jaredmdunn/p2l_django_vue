from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    dob = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse('my-account')

class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    review = models.TextField(max_length=250)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )

    def get_absolute_url(self):
        return(reverse('pages:homepage'))

    def __str__(self):
        return self.review
