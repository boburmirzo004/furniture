from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser

User = get_user_model()


class CustomUserCreationForms(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'username')
        labels = {
            'email': _('Email'),
            'full_name': _('Full name'),
            'username': _('Username'),
        }
        help_texts = {
            'email': _('Enter a valid email address'),
            'full_name': _('Enter your full name'),
            'username': _('Choose a unique username'),
        }
        error_messages = {
            'email': {
                'required': _('Email is required'),
                'invalid': _('Enter a valid email address'),
            },
            'username': {
                'required': _('Username is required'),
                'unique': _('This username is already taken'),
            },
        }


class CustomAuthenticationForm(forms.Form):
    identifier = forms.CharField(
        max_length=128,
        label=_('Username or Email')
    )
    password = forms.CharField(
        max_length=128,
        label=_('Password'),
        widget=forms.PasswordInput
    )

    def clean(self):
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
        except User.DoesNotExist:
            raise forms.ValidationError(
                _('User not found, please check your credentials')
            )

        credentials = {'username': identifier, 'password': password}
        user_in = authenticate(**credentials)
        if user_in is None:
            raise forms.ValidationError(
                _('User not found, please check your credentials')
            )

        self.cleaned_data['user'] = user_in
        return self.cleaned_data