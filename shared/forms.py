from django import forms

from shared.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        exclude = ['id','is_read','created_at','updated_at']


    def clean_message(self):
        message  = self.cleaned_data.get('message')
        if 'hello' in message.lower():
            raise forms.ValidationError('Hello can not be inside message')
        return message