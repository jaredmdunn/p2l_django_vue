from django.urls import path
from .views import AboutUsView, ContactUsView, HomePageView, ContactUsThanksView


app_name = 'pages'
urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about-us'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('contact/thanks', ContactUsThanksView.as_view(), name='thanks'),
    path('', HomePageView.as_view(), name='homepage'),
]
