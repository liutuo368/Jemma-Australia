from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.context_processors import csrf

from Home_app.models import Tradie
from Home_app.models import Customer
from Home_app.models import Order
from Home_app.models import TradieJobType
from Home_app.models import Rating
from Home_app.models import MyUser
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


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("index")


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
            "address": str(tradie.address1 + " " + tradie.suburb + " " + tradie.state + " " + tradie.postcode),
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


def customer_search_result(request):
    login_status = False
    if request.user.is_authenticated:
        login_status = True
    job_type = request.GET["job_type"]
    location = request.GET["location"]
    job_type_list = TradieJobType.objects.filter(jobType=job_type)
    tradie_list = []
    for var in job_type_list:
        if var.tradie.suburb == location:
            rating_list = Rating.objects.filter(user=var.tradie.myUser)
            if len(rating_list) > 0:
                sum_rating = 0
                for rating in rating_list:
                    sum_rating += rating.points
                tradie_list.append((var, round(sum_rating / len(rating_list), 1)))
            else:
                tradie_list.append((var, len(rating_list), 5))

    context = {
        "login_status": json.dumps(login_status),
        "tradie_list": tradie_list
    }
    return render(request, "Customer/customer_search_result.html", context)


def tradie_detail(request):
    tradie_id = request.GET["tradie_id"]
    tradie = Tradie.objects.get(myUser_id=int(tradie_id))
    rating_list = Rating.objects.filter(user=tradie.myUser)
    avg_rating = 5
    if len(rating_list) > 0:
        sum_rating = 0
        for rating in rating_list:
            sum_rating += rating.points
        avg_rating = round(sum_rating / len(rating_list), 1)
    context = {
        "tradie": tradie,
        "rating_number": len(rating_list),
        "rating": avg_rating
    }
    return render(request, "Customer/tradie_detail.html", context)


def tradie_detail1(request):
    return render(request, "Customer/tradie_detail1.html")


def tradie_detail2(request):
    return render(request, "Customer/tradie_detail2.html")


def tradie_detail3(request):
    return render(request, "Customer/tradie_detail3.html")


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


def update_profile(request):
    tradie = Tradie.objects.get(myUser=request.user)
    Your_Description = request.POST["Your_Description"]
    tradie.description = Your_Description
    Your_FullName = request.POST["Your_FullName"]
    FirstName = Your_FullName.split(" ", 1)[0]
    LastName = Your_FullName.split(" ", 1)[-1]
    tradie.first_name = FirstName
    tradie.last_name = LastName

    Your_Address = request.POST["Your_Address"]

    Address = Your_Address.split()
    tradie.suburb = Address[-3]
    tradie.state = Address[-2]
    tradie.postcode = Address[-1]
    str = ' '
    tradie.address1 = str.join(Address[0:-3])
    Your_Number = request.POST["Your_Number"]
    tradie.phone = Your_Number

    Your_CompanyName = request.POST["Your_CompanyName"]
    tradie.company = Your_CompanyName

    Your_CompanyABN = request.POST["Your_CompanyABN"]
    tradie.ABN = Your_CompanyABN

    Your_BSB = request.POST["Your_BSB"]
    tradie.BSB = Your_BSB

    Your_BankNumber = request.POST["Your_BankNumber"]
    tradie.accountNo = Your_BankNumber

    Your_BankName = request.POST["Your_BankName"]
    tradie.accountName = Your_BankName

    tradie.save()
    return HttpResponseRedirect("tradie_profile")


def updatehp(request):
    return HttpResponse()
