import threading
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _

from users.forms import CustomUserCreationForms, CustomAuthenticationForm
from users.utils import email_verification_token

User = get_user_model()


def account_page_view(request):
    return render(request, 'users/account.html')


def register_page_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForms(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user=user)
            link = request.build_absolute_uri(
                reverse(viewname='users:verify-email', kwargs={'uidb64': uid, 'token': token})
            )

            # Send email
            thread = threading.Thread(target=send_mail, kwargs={
                'subject': _("Verify your email"),
                'message': _("Click the link to verify your account: ") + link,
                'from_email': "noreply@yourapp.com",
                'recipient_list': [user.email],
            })
            thread.start()

            messages.success(
                request,
                _('We sent a confirmation link to your email. Please verify it.')
            )
            return redirect('shared:home')

        else:
            error_messages = ', '.join([f"{field}: {', '.join(errors)}"
                                        for field, errors in form.errors.items()])
            messages.error(request, _(error_messages))
            return render(request, 'users/register.html')

    else:
        return render(request, 'users/register.html')


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:register')

    else:
        messages.error(request, _('Something went wrong. Please try again later.'))
        return render(request, 'users/login.html')


def login_page_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('shared:home')
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")

            error_text = " | ".join(errors)
            messages.error(request, _(error_text))
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')


def reset_password_page_view(request):
    return render(request, 'users/reset-password.html')