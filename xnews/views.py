from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User

# Create your views here.


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


def xnews_home(request):

    # access as a user or tourist
    email = request.COOKIES.get('email', '')
    if email:
        user = get_object_or_404(User, email=email)
    else:
        user = None

    return render_to_response(
        'xnews_home.html',
        {'user': user},
        context_instance=RequestContext(request)
    )


def xnews_register(request):

    # check if login
    email = request.COOKIES.get('email', '')
    user = User.objects.filter(email=email)
    if user:
        return render_to_response(
            'xnews_home.html',
            {'user': user},
            context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # get the form data
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            # check email
            filterResult = User.objects.filter(email=email)
            if filterResult:
                return render_to_response(
                    'xnews_register.html',
                    {'registerform': form, 'error': 'Email Used!'},
                    context_instance=RequestContext(request)
                )
            # check password
            else:
                if password != password2:
                    return render_to_response(
                        'xnews_register.html',
                        {'registerform': form, 'error': 'Inconsistent Password!'},
                        context_instance=RequestContext(request)
                    )

            # create user account
            User.objects.create(email=email, username=username, password=password)
            return HttpResponse('Register Success!')
    else:
        form = RegisterForm()
        return render_to_response(
            'xnews_register.html',
            {'registerform': form},
            context_instance=RequestContext(request)
        )


def xnews_login(request):

    # check if login
    email = request.COOKIES.get('email', '')
    user = User.objects.filter(email=email)
    if user:
        return render_to_response(
            'xnews_home.html',
            {'user': user,},
            context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the form data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # check password
            user = User.objects.filter(email__exact=email, password__exact=password)
            if user:
                response = HttpResponseRedirect('/xnews/')
                response.set_cookie('email', email, 3600)
                return response
            else:
                # login failed
                return render_to_response(
                    'xnews_login.html',
                    {'loginform': form, 'error': 'Wrong Email or Password!'},
                    context_instance=RequestContext(request)
                )
    else:
        form = LoginForm()
        return render_to_response(
            'xnews_login.html',
            {'loginform': form},
            context_instance=RequestContext(request)
        )


def xnews_logout(request):
    response = HttpResponseRedirect('/xnews/')
    response.delete_cookie('email')
    return response