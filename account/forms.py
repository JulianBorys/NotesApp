from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text="Password must meet the complexity requirements."
    )
    password_confirm = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        """
        Validates the password using Django's password validators.
        """
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)  # Sprawdza wszystkie zdefiniowane walidatory hasła
        except ValidationError as e:
            raise forms.ValidationError(e.messages)  # Dodaje komunikaty o błędach do formularza
        return password

    def clean_password_confirm(self):
        """
        Ensures that both password fields match.
        """
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_confirm'):
            raise forms.ValidationError("Passwords do not match.")
        return cd['password_confirm']
