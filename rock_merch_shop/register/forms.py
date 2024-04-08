from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'email')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)