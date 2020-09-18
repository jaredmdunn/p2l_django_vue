from django.urls import path

from .views import MyAccountPageView

app_name = 'users'
urlpatterns = [
    path('my-account/', MyAccountPageView.as_view(), name='my-account'),
]