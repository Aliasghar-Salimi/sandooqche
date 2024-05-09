from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

import urllib
from django.conf import settings
import json
from json import JSONEncoder

from django.utils.crypto import get_random_string

from time import gmtime, strftime

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm
from .utils import grecaptcha_verify, RateLimited, get_client_ip
from .models import Token

# Creating a token containing 48 charecter
import string, random
char_set = string.ascii_letters + string.digits
create_token = lambda: ''.join(random.sample(char_set, 48))

# Views

def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': '''متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است،
                             از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'''}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, self.template_name, context)
        
        if form.is_valid():
            # if not grecaptcha_verify(request):  # captcha was not correct
            #     # context = {
            #     #     'message': 'captcha was not crrect, refill the form and do the captcha, please'}
            #     # return render(request, 'users/register.html', context)
            #     message = 'captcha was not crrect, refill the form and do the captcha, please'
            #     messages.error(request, message)
            # else:
            #     this_user = form.save()
            this_user = form.save()

            this_token = create_token()
            Token.objects.create(user=this_user, token=this_token)

            username = form.cleaned_data.get('username')
            messages.success(request, f'''Account created for {username}, this is your token {this_token}.
                              please remember it, submit expences and incomes dipends on it :)''')
            
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm
    global form

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)    
    
    # def get_success_url(self):
    #     message = 'you successfuly loged in :)'
    #     return super().get_success_url()
    
    def post(self, request):
        
        if 'username' and 'password' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            this_user = User.objects.get(username=username)
            
            if check_password(password, this_user.password):

                if not Token.objects.filter(user=this_user).exists():
                    token = get_random_string(48)
                    this_token = Token.objects.create(user=this_user, token=token)
                    this_token.save()
                    context = {
                        'message': f'your token created, it\'s "{this_token.token}" please remember it, it never shown again'
                    }
                    return JsonResponse(context ,JSONEncoder)
                else:
                    this_token = get_object_or_404(Token, user=this_user)
                    context = {
                        'message': f'your token is \'{this_token.token}\' please remember it'
                    }
                    return JsonResponse(context ,JSONEncoder)
                                
        return super(CustomLoginView, self).post(request)

            # return super(CustomLoginView, self).form_valid(form)

                # if not Token.objects.filter(user=this_user).exists():
                #     token = create_token()
                #     this_token = Token.objects.create(user=this_user, token=token)
                #     return JsonResponse({'token': this_token.token}, encoder=JSONEncoder)
                # else:
                #     try:
                #         this_token = get_object_or_404(Token, user=this_user)
                #         return JsonResponse({'token': this_token.token}, encoder=JSONEncoder)
                #     except Http404:
                #         return JsonResponse({'token': this_token.token}, encoder=JSONEncoder)

                
                
                # global this_token
                # try:        
                #     this_token = get_object_or_404(Token, user=this_user)
                # except http404:
                #     token = create_token()
                #     this_token = Token.objects.create(user=this_user, token=token)

        # login(request, this_user)
        # this_token, _ = Token.objects.get_or_create(user=this_user)

        
        # if user is not None:
        #     login(request, user)
        #     token = create_token()
        #     Token.objects.create(user=user, token=token)
        #     return super(CustomLoginView, self).form_valid(form)
        # else:
        #     # Handle invalid login attempt
        #     return JsonResponse({'error': 'Invalid credentials'}, status=401)

