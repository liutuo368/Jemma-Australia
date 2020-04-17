from django.shortcuts import render
from django.http import HttpResponse
from .models import Tradie

# Create your views here.

def index(request):

    return render(request, "HTML/home.html")

def login(request):

    return render(request, "HTML/login.html")

def about_us(request):

    return render(request, "HTML/about_us.html")

def contact(request):

    return render(request, "HTML/contact.html")


def tradie_profile(request):

    return render(request, "HTML/home.html")


def tradie_history(request):

    return render(request, "HTML/tradie_history.html")


def tradie_current_job(request):

    return render(request, "HTML/tradie_current_job.html")

