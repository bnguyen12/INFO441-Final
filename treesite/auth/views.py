from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrationForm, SigninForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def register(request):
    """ lets new users register and create a new profile """
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, "auth/register.html", {'form':form}, status=200)
    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password']
            pwdconf = form.cleaned_data['passwordconf']
            if pwd == pwdconf:
                user = User.objects.create_user(
                    form.cleaned_data["email"],
                    form.cleaned_data["password"],
                    first_name = form.cleaned_data["first_name"],
                    last_name = form.cleaned_data["last_name"],
                    perm_type = form.cleaned_data["perm_type"]
                )
                return HttpResponseRedirect("/auth/signin")
            else:
                return HttpResponse("Passwords did not match.", status=400)
        else:
            return HttpResponse("Invalid registration request.", status=400)
    else:
        return HttpResponse("Method not allowed on auth/register.", status=405)

@csrf_exempt
def signin(request):
    """ lets old users sign into their accounts """
    if request.method == 'GET':
        form = SigninForm()
        return render(request, "auth/signin.html", {'form':form}, status=200)
    elif request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            pwd = form.cleaned_data["password"]
            user = authenticate(username = email, password = pwd)
            if user is None:
                return HttpResponse("Invalid credentials.", status=401)
            else:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return HttpResponse("Bad login form.", status=400)
    else:
        return HttpResponse("Method not allowed on auth/register.", status=405)

def signout(request):
    """ lets users signout of their accounts """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse("User not logged in.", status=200)
        else:
            logout(request)
            return HttpResponse("Sign out successful.", status=200)
    else:
        return HttpResponse("Method not allowed on auth/signout.", status=405)