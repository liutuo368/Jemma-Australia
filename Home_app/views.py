from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .models import MyUser

# Create your views here.


def index(request):

    return render(request, "Home/home.html")


def login(request):
    username = request.POST["uname"]
    password = request.POST["pswd"]
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect("tradie")
    else:
        return HttpResponseRedirect("index")


def about_us(request):

    return render(request, "Home/about_us.html")


def contact(request):

    return render(request, "Home/contact.html")


def tradie_profile(request):

    return render(request, "Tradie/tradie_profile.html")


def tradie_history(request):

    return render(request, "Tradie/tradie_history.html")


def tradie_current_job(request):

    return render(request, "Tradie/tradie_current_job.html")


def top_menu_without_sign_in(request):

    return render(request, "SubTemplate/top_menu_without_sign_in.html")


def top_menu_sign_in(request):
    return render(request, "SubTemplate/top_menu_sign_in.html")
