from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User, Category, PrivateCategory, Post

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
        # get private category list
        privatecategories = user.privatecategory_set.all()
        items = []
        for privatecategory in privatecategories:
            if privatecategory.count >= 0:
                category = Category.objects.get(category=privatecategory.category)
                post = category.post_set.first()
                item = {'category': category, 'post': post}
                items.append(item)

    else:
        user = None
        # get all category list
        categories = Category.objects.all()
        items = []
        for category in categories:
            post = category.post_set.first()
            item = {'category': category, 'post': post}
            items.append(item)

    ctx = {
        'user': user,
        'items': items
    }

    return render_to_response(
        'xnews_home.html',
        ctx,
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
            if password != password2:
                return render_to_response(
                    'xnews_register.html',
                    {'registerform': form, 'error': 'Inconsistent Password!'},
                    context_instance=RequestContext(request)
                )

            # create user account
            user = User.objects.create(email=email, username=username, password=password)
            # create private category list, default as all
            categories = Category.objects.all()
            for category in categories:
                PrivateCategory.objects.create(email=user, category=category)

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


class SettingForm(forms.Form):
    username = forms.CharField(label='username', max_length=64)
    introduction = forms.CharField(label='introduction', max_length=128)


def xnews_setting(request):

    # check if login
    email = request.COOKIES.get('email', '')
    user = User.objects.filter(email=email)
    if not user:
        return HttpResponseRedirect('/xnews/login/')

    if request.method == 'POST':
        form = SettingForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            introduction = form.cleaned_data['introduction']
            choices = request.POST.getlist('category_list')

            # update user information
            user.update(username=username, introduction=introduction)

            # update private category list
            categories = Category.objects.all()
            for category in categories:
                if category.category in choices:
                    private_category = PrivateCategory.objects.filter(email=user, category=category)
                    if private_category.get().count < 0:
                        private_category.update(count=1000)
                else:
                    private_category = PrivateCategory.objects.filter(email=user, category=category)
                    if private_category.get().count >= 0:
                        private_category.update(count=-1)

            private_categories = PrivateCategory.objects.filter(email=user)
            ctx = {
                'message': 'Setting Updated.',
                'user': user.get(),
                'private_categories': private_categories,
                'choices': choices,
            }

            return render_to_response(
                'xnews_setting.html',
                ctx,
                context_instance=RequestContext(request)
            )

    private_categories = PrivateCategory.objects.filter(email=user)
    ctx = {
        'user': user.get(),
        'private_categories': private_categories,
    }

    return render_to_response(
        'xnews_setting.html',
        ctx,
        context_instance=RequestContext(request)
    )


def xnews_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all()

    # check if login
    email = request.COOKIES.get('email', '')
    user = User.objects.filter(email=email)
    if user:
        user = user.get()
    else:
        user = None

    ctx = {
        'category': category,
        'posts': posts,
        'user': user,
    }

    return render_to_response(
        'xnews_category.html',
        ctx,
        context_instance=RequestContext(request)
    )


def xnews_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category = Category.objects.get(category=post.category)

    # check if login
    email = request.COOKIES.get('email', '')
    user = User.objects.filter(email=email)
    if user:
        user = user.get()
    else:
        user = None

    ctx = {
        'post': post,
        'user': user,
        'category': category
    }

    return render_to_response(
        'xnews_post.html',
        ctx,
        context_instance=RequestContext(request)
    )