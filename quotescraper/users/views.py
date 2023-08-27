from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm


def signup(request):
    """
    The signup function is a view that handles the signup process.
    It first checks if the user is already authenticated, and if so, redirects them to the root page.
    If not, it checks whether or not there was a POST request made to this function (i.e., someone submitted data).
    If so, it creates an instance of RegisterForm with that data and validates it; if valid, saves the form's information as a new User object in our database and redirects them to root; otherwise renders users/signup.html with context {'form': form} (the invalid form). If no POST request
    
    :param request: Get the request data from the client
    :return: A redirect to the root route if a user is already logged in
    :doc-author: Trelent
    """
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'users/signup.html', context={'form': form})

    return render(request, 'users/signup.html', context={'form': RegisterForm()})


def login_user(request):
    """
    The login_user function is a view that handles the login process.
    It checks if the user is already authenticated, and if so redirects them to the root page.
    If not, it checks whether or not there was a POST request made (i.e., someone submitted data).
    If so, it authenticates the user with authenticate() using their username and password from request.POST['username'] and request.POST['password']. If authentication fails (user is None), then an error message will be displayed on screen saying &quot;Username or password didn't match&quot;. Otherwise, we log in our user with login(request, user
    
    :param request: Get the current request
    :return: A redirect to the root route if the user is already authenticated
    :doc-author: Trelent
    """
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes:root')

    return render(request, 'users/login.html', context={'form': LoginForm})


@login_required
def logout_user(request):
    """
    The logout_user function is a view that logs out the user and redirects them to the root page.
    It takes in one parameter, request, which is an HttpRequest object. It returns an HttpResponseRedirect object.
    
    :param request: Get the user's session
    :return: A redirect to the root route
    :doc-author: Trelent
    """
    logout(request)
    return redirect(to='quotes:root')




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
