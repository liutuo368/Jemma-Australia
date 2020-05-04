from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Home_app.models import Tradie
from Home_app.models import Customer

# Create your views here.


def index(request):

    return render(request, "Home/home.html")


def login(request):
    username = request.POST["uname"]
    password = request.POST["pswd"]
    user_type = request.POST["optionsRadiosinline"]
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user_type == "tradie":
            try:
                Tradie.objects.get(myUser=user)
                auth.login(request, user)
                return HttpResponseRedirect("tradie")
            except Tradie.DoesNotExist:
                raise Http404("Tradie does not exist")
        elif user_type == "customer":
            try:
                Customer.objects.get(myUser=user)
                auth.login(request, user)
                return HttpResponseRedirect("index")
            except Customer.DoesNotExist:
                raise Http404("Customer does not exist")
    else:
        raise Http404("User does not exist")


def about_us(request):

    return render(request, "Home/about_us.html")


def contact(request):

    return render(request, "Home/contact.html")


def terms_and_conditions(request):

    return render(request, "Home/terms_and_conditions.html")


def tradie_profile(request):
    try:
        tradie = Tradie.objects.get(myUser=request.user)
    except Tradie.DoesNotExist:
        raise Http404("Tradie does not exist")
    context = {
        "description": tradie.description,
        "fullname": tradie.first_name + " " + tradie.last_name,
        "address": tradie.address1 + " " + tradie.suburb + " " + tradie.state + " " + tradie.postcode,
        "phone": tradie.phone,
        "company": tradie.company,
        "ABN": tradie.ABN,
        "BSB": tradie.BSB,
        "accountNo": tradie.accountNo,
        "accountName": tradie.accountName
    }
    return render(request, "Tradie/tradie_profile.html", context)


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
