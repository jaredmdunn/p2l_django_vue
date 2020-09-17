from django.urls import path

from .views import MyAccountPageView

urlpatterns = [
    path('my-account/', MyAccountPageView.as_view(), name='my-account'),
]