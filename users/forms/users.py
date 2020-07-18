""" User Forms """
# Django
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
# Models
from users.models import User
from users.models import Profile


class SignupForm(forms.Form):
    """ Signup form """

    username = forms.CharField(min_length=4, max_length=50)

    password = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """ Username must be unique. """
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already use')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()
        if not data.get('password') and not data.get('password_confirmation'):
            raise forms.ValidationError('Password or Password confirmation was not provided')
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self):
        """ Create user and profile"""
        user = self.cleaned_data
        user.pop('password_confirmation')

        user = User.objects.create_user(**user)
        profile = Profile(user=user)
        profile.save()



