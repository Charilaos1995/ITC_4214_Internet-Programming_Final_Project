from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(UserChangeForm):
    """
    A form for updating a user's basic information.

    Inherits from UserChangeForm but excludes the password field,
    allowing users to update their username and email address without changing their password.
    """
    password = None  # Exclude the password field from the form

    class Meta:
        model = User
        fields = ('username', 'email')  # Fields to be included in the form.

class ContactForm(forms.Form):
    """
    A simple contact form for user communication.

    This form collects a user's name, email, and message for communication purposes.
    The message field uses a Textarea widget for multiline input.
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)