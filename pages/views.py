from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/homepage.html'

class AboutUsView(TemplateView):
    template_name = 'pages/about.html'

class ContactUsView(TemplateView):
    template_name = 'pages/contact.html'
