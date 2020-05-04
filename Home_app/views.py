from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

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


def terms_and_conditions(request):

    return render(request, "Home/terms_and_conditions.html")


def tradie_profile(request):

    return render(request, "Tradie/tradie_profile.html")


def tradie_history(request):

    return render(request, "Tradie/tradie_history.html")


def tradie_current_job(request):

    return render(request, "Tradie/tradie_current_job.html")


def tradie_calendar(request):

    return render(request, "Tradie/tradie_calendar.html")


def top_menu_without_sign_in(request):

    return render(request, "SubTemplate/top_menu_without_sign_in.html")


def top_menu_sign_in(request):

    return render(request, "SubTemplate/top_menu_sign_in.html")

def footer(request):

    return render(request, "SubTemplate/footer.html")

def side_menu(request):

    return render(request, "SubTemplate/side_menu.html")

def updatehp(request):
    return HttpResponse()
