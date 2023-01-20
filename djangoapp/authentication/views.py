from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from authentication.forms import LogInForm, SignUpForm


def login_page(request: HttpRequest) -> HttpResponse:
    form: LogInForm = LogInForm()
    message: str = ""

    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flow')
            
            else:
                message = "Identifiants invalides."

    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form: SignUpForm = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'authentication/signup.html', context={'form': form})
