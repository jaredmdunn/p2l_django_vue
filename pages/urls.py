from django.urls import path
from .views import AboutUsView, ContactUsView, HomePageView


app_name = 'pages'
urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about-us'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('', HomePageView.as_view(), name='homepage'),
]