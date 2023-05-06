from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from basic_app import forms, models
from basic_app.forms import UserProfileInfoForm


# Create your views here.
def index(request):
    return render(request, "basic_app/index.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def special(request):
    return HttpResponse("You are logged in")


def register(request):
    registered = False
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    context = {
        "registered": registered,
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "basic_app/register.html", context=context)


def user_login(request):
    print(f"user login with request {request}")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Authenticating user {username} {password}")

        user = authenticate(username=username, password=password)
        print(f"user: {user}")
        if user:
            if user.is_active:
                print("user active")
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Your account is not active")
        else:
            print("Someone tried to login and failed")
            print(f"Username: {username}, password: {password}")
            return HttpResponse("Invalid login")
    else:
        return render(request, "basic_app/login.html")
