from modeltranslation.translator import TranslationOptions, register

from shared.models import AboutUs, Contact


@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('name', 'profession', 'info',)


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('full_name', 'email', 'subject', 'message',)
