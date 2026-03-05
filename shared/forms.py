from django import forms
from django.utils.translation import gettext_lazy as _
from shared.models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['id', 'is_read', 'created_at', 'updated_at']

        # Agar modelda verbose_name bo‘lmasa, shu yerda label berish mumkin
        labels = {
            "name": _("Full name"),
            "email": _("Email"),
            "message": _("Message"),
        }

        help_texts = {
            "message": _("Write your message here"),
        }

        error_messages = {
            "name": {
                "required": _("Full name is required"),
            },
            "email": {
                "required": _("Email is required"),
                "invalid": _("Enter a valid email address"),
            },
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')

        if message and 'hello' in message.lower():
            raise forms.ValidationError(
                _("The word 'hello' is not allowed inside the message.")
            )

        return message