from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from saleor.cart.utils import find_and_assign_anonymous_cart

from .forms import LoginForm, PasswordSetUpForm, SignupForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage

@find_and_assign_anonymous_cart()
def login(request):
    kwargs = {
        'template_name': 'account/login.html', 'authentication_form': LoginForm}
    return django_views.LoginView.as_view(**kwargs)(request, **kwargs)


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect(settings.LOGIN_REDIRECT_URL)


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
<<<<<<< HEAD
        to_email = 'rupesh171198@gmail.com'
        email = EmailMessage(
            'test subject', 'test mail', to=[to_email]
        )
        email.send()
        #send_mail('Subject here', 'Here is the message.', 'testdreahouse@gmail.com', ['rupesh171198@gmail.com'], fail_silently=False)

=======
>>>>>>> bca2e6f1e1eb786a14f49417757fd8ac17254368
        user = auth.authenticate(
            request=request, email=email, password=password)
        if user:
            auth.login(request, user)
        messages.success(request, _('User has been created'))
        redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(redirect_url)
    ctx = {'form': form}
    return TemplateResponse(request, 'account/signup.html', ctx)


def password_reset(request):
    kwargs = {
        'template_name': 'account/password_reset.html',
        'success_url': reverse_lazy('account_reset_password_done'),
        'email_template_name': 'account/email/password_reset_message.txt',
        'subject_template_name': 'account/email/password_reset_subject.txt'}
    return django_views.PasswordResetView.as_view(**kwargs)(request, **kwargs)


class PasswordResetConfirm(django_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_from_key.html'
    success_url = reverse_lazy('account_reset_password_complete')
    set_password_form = PasswordSetUpForm
    token = None
    uidb64 = None


def password_reset_confirm(request, uidb64=None, token=None):
    kwargs = {
        'template_name': 'account/password_reset_from_key.html',
        'success_url': reverse_lazy('account_reset_password_complete'),
        'set_password_form': 'PasswordSetUpForm',
        'token': token,
        'uidb64': uidb64}
    return PasswordResetConfirm.as_view(**kwargs)(
        request, **kwargs)
