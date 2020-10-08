from django import forms


class ContactUsForm(forms.Form):
    """The Contact Us Form"""
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g., name@example.com'})
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '5', 'placeholder': 'Message'})
    )
