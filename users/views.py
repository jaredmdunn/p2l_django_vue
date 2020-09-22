from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from allauth.account.views import PasswordChangeView

from .forms import CustomUserChangeForm

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('my-account')

class MyAccountPageView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    success_message = 'Update Successful'
    template_name = 'account/my_account.html'

    def get_object(self):
        return self.request.user
