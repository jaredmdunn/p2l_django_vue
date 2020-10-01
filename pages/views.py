from django.views.generic import TemplateView


class VuePageView(TemplateView):
    template_name = 'vue-test.html'


class HomePageView(TemplateView):
    template_name = 'pages/homepage.html'


class AboutUsView(TemplateView):
    template_name = 'pages/about.html'


class ContactUsView(TemplateView):
    template_name = 'pages/contact.html'
