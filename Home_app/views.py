from django.shortcuts import render
from django.http import HttpResponse
from .models import Tradie

# Create your views here.


def index(request):

    return render(request, "Home/home.html")


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


def menu(request):
    return render(request, "SubTemplate/top_menu_without_sign_in.html")


