from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Home_app.models import Tradie
from Home_app.models import Customer
from Home_app.models import Order
from django.db.models import Q
import json

def index(request):
    context = {
        "login_status": json.dumps(request.user.is_authenticated)
    }
    return render(request, "Home/home.html", context)


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
    context = {
        "login_status": json.dumps(request.user.is_authenticated)
    }
    return render(request, "Home/about_us.html", context)


def contact(request):
    context = {
        "login_status": json.dumps(request.user.is_authenticated)
    }
    return render(request, "Home/contact.html", context)


def terms_and_conditions(request):
    context = {
        "login_status": json.dumps(request.user.is_authenticated)
    }
    return render(request, "Home/terms_and_conditions.html", context)


def tradie_profile(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        context = {
            "login_status": json.dumps(True),
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
    else:
        raise Http404("Haven't logged in")


def tradie_history(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        job_history = Order.objects.filter(Q(tradie=tradie), Q(orderStatus="Rejected") | Q(orderStatus="Completed"))
        context = {
            "login_status": json.dumps(True),
            "job_history": job_history
        }
        return render(request, "Tradie/tradie_history.html", context)
    else:
        raise Http404("Haven't logged in")


def tradie_current_job(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        current_jobs = Order.objects.filter(Q(tradie=tradie), Q(orderStatus="Pending") | Q(orderStatus="Accepted"))
        context = {
            "login_status": json.dumps(True),
            "current_jobs": current_jobs
        }
        return render(request, "Tradie/tradie_current_job.html", context)
    else:
        raise Http404("Haven't logged in")


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
