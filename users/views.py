from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from allauth.account.views import PasswordChangeView

from .forms import CustomUserChangeForm, ReviewForm
from .models import Review


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """The custom password change view"""
    success_url = reverse_lazy('my-account')


class MyAccountPageView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """The my account page view"""
    model = get_user_model()
    form_class = CustomUserChangeForm
    success_message = 'Update Successful'
    template_name = 'account/my_account.html'

    def get_object(self):
        return self.request.user


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """The review create view"""
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
