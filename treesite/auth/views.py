from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrationForm, SigninForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
from main.models import Permissions

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
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                    email=form.cleaned_data["email"],
                    first_name = form.cleaned_data["first_name"],
                    last_name = form.cleaned_data["last_name"],
                    # perm_type = form.cleaned_data["permission_type"]
                )
                newPermissionObject = Permissions(
                    user_id=user,
                    perm_type=form.cleaned_data["permission_type"]
                )
                print(user)
                print(user.password)
                newPermissionObject.save()
                return HttpResponseRedirect("signin")
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
            username = form.cleaned_data["username"]
            pwd = form.cleaned_data["password"]
            print(pwd)
            print(username)
            user = authenticate(username = username, password = pwd)
            print(user)
            if user is None:
                return HttpResponse("Invalid credentials.", status=401)
            else:
                login(request, user)
                return HttpResponseRedirect("main/adopt")
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
        return HttpResponse("Method not allowed.", status=405)