from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from common.utils.email import send_email
from .forms import ContactUsForm


class HomePageView(TemplateView):
    """The homepage view"""
    template_name = 'pages/homepage.html'


class AboutUsView(TemplateView):
    """The about us view"""
    template_name = 'pages/about.html'


class ContactUsView(FormView):
    """The contact us form view"""
    template_name = 'pages/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('pages:thanks')

    def form_valid(self, form):
        """Overrides form_valid to send an email to the admin with the form data."""
        data = form.cleaned_data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        user_subject = data['subject']
        message = data['message']

        subject = 'Play2Learn - Contact Us Form Submission'
        content = f'''<p>Hey p2ladmin!</p>
            <p>{ first_name } { last_name } ({ email }) 
            is contacting you about { user_subject }</p>
            <p>Message:</p>
            <p>{ message }</p>'''

        send_email(settings.DEFAULT_FROM_EMAIL, subject, content)
        return super().form_valid(form)


class ContactUsThanksView(TemplateView):
    """The success page view for submitting the contact us form"""
    template_name = 'pages/thanks.html'
