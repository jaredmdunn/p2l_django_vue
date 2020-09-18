from django.urls import path

from .views import MyAccountPageView, ReviewCreateView

urlpatterns = [
    path('my-account/', MyAccountPageView.as_view(), name='my-account'),
    path('review/create/', ReviewCreateView.as_view(), name='create'),
]