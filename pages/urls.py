from django.urls import path
from .views import AboutUsView, ContactUsView, HomePageView, VuePageView


app_name = 'pages'
urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about-us'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('vue', VuePageView.as_view(), name='vue-page'),
    path('', HomePageView.as_view(), name='homepage'),
]
