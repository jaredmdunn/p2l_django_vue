from django.urls import path
from .views import AboutUsView, ContactUsView, HomePageView


app_name = 'pages'
urlpatterns = [
    path('about/', AboutUsView.as_view(), 'about-us'),
    path('contact/', ContactUsView.as_view(), 'contact-us'),
    path('', HomePageView.as_view(), 'homepage'),
]