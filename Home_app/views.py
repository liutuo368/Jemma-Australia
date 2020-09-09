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
import Jemma.Encrypt as en


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
    if "remember_me" not in request.POST:
        request.session.set_expiry(0)
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


def sign_up(request):
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    email = request.POST["email"]
    password = request.POST["password"]
    user_type = request.POST["userOptions"]

    try:
        MyUser.objects.get(email=email)
        raise Http404("Email alreay been registered")
    except MyUser.DoesNotExist:
        myUser = MyUser(email=email, date_of_birth='2020-1-1', user_type=user_type, password=password)
        myUser.save()
        if user_type == "tradie":
            tradie = Tradie(myUser=myUser, first_name=firstname, last_name=lastname, accountStatus="Active", travelDistance=0)
            tradie.save()
            auth.login(request, myUser)
            return HttpResponseRedirect("tradie")
        else:
            customer = Customer(myUser=myUser, first_name=firstname, last_name=lastname, accountStatus="Active")
            customer.save()
            auth.login(request, myUser)
            return HttpResponseRedirect("index")


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
        ABN = tradie.ABN
        BSB = tradie.BSB
        accountNo = tradie.accountNo
        accountName = tradie.accountName
        if BSB is not None and BSB != "":
            BSB = en.decrypt(BSB)
        if accountNo is not None and accountNo != "":
            accountNo = en.decrypt(accountNo)
        if accountName is not None and accountName != "":
            accountName = en.decrypt(accountName)

        context = {
            "login_status": json.dumps(True),
            "description": tradie.description,
            "fullname": tradie.first_name + " " + tradie.last_name,
            "address": str(tradie.address1 + " " + tradie.suburb + " " + tradie.state + " " + tradie.postcode),
            "phone": tradie.phone,
            "company": tradie.company,
            "ABN": ABN,
            "BSB": BSB,
            "accountNo": accountNo,
            "accountName": accountName
        }
        return render(request, "Tradie/tradie_profile.html", context)
    else:
        raise Http404("Haven't logged in")


def customer_profile(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(myUser=request.user)
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")

        cardHolder = customer.cardHolder
        cardNo = customer.cardNo
        cardValidDate = customer.cardValidDate
        if cardHolder is not None and cardHolder != "":
            cardHolder = en.decrypt(cardHolder)
        if cardNo is not None and cardNo != "":
            cardNo = en.decrypt(cardNo)
        if cardValidDate is not None and cardValidDate != "":
            cardValidDate = en.decrypt(cardValidDate)

        context = {
            "login_status": json.dumps(True),
            "fullname": customer.first_name + " " + customer.last_name,
            "address": str(customer.address1 + " " + customer.suburb + " " + customer.state + " " + customer.postcode),
            "phone": customer.phone,
            "cardHolder": cardHolder,
            "cardNo": cardNo,
            "cardValidDate": cardValidDate
        }
        return render(request, "Customer/customer_profile.html", context)
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


def tradie_calendar(request):
    return render(request, "Tradie/tradie_calendar.html")

def tradie_quotes(request):
    return render(request, "Tradie/tradie_quotes.html")

def top_menu_without_sign_in(request):
    return render(request, "SubTemplate/top_menu_without_sign_in.html")


def top_menu_sign_in(request):
    return render(request, "SubTemplate/top_menu_sign_in.html")


def footer(request):
    return render(request, "SubTemplate/footer.html")


def side_menu(request):
    return render(request, "SubTemplate/side_menu.html")

def side_menu_customer(request):
    return render(request, "SubTemplate/side_menu_customer.html")


def update_tradie_profile(request):
    tradie = Tradie.objects.get(myUser=request.user)
    tradie.description = request.POST["description"]
    full_name = request.POST["fullName"]
    first_name = full_name.split(" ", 1)[0]
    last_name = full_name.split(" ", 1)[-1]
    tradie.first_name =first_name
    tradie.last_name = last_name

    address = request.POST["address"]

    address = address.split()
    tradie.suburb = address[-3]
    tradie.state = address[-2]
    tradie.postcode = address[-1]
    str = ' '
    tradie.address1 = str.join(address[0:-3])
    number = request.POST["number"]
    tradie.phone = number

    company_name = request.POST["companyName"]
    tradie.company = company_name

    company_ABN = request.POST["companyABN"]
    tradie.ABN = company_ABN

    BSB = en.encrypt(request.POST["BSB"])
    tradie.BSB = BSB

    bank_number = en.encrypt(request.POST["bankNumber"])
    tradie.accountNo = bank_number

    bank_name = en.encrypt(request.POST["bankName"])
    tradie.accountName = bank_name

    tradie.save()
    return HttpResponseRedirect("tradie_profile")


def update_customer_profile(request):
    customer = Customer.objects.get(myUser=request.user)
    full_name = request.POST["fullName"]
    first_name = full_name.split(" ", 1)[0]
    last_name = full_name.split(" ", 1)[-1]
    customer.first_name = first_name
    customer.last_name = last_name

    address = request.POST["address"]

    address = address.split()
    customer.suburb = address[-3]
    customer.state = address[-2]
    customer.postcode = address[-1]
    str = ' '
    customer.address1 = str.join(address[0:-3])
    number = request.POST["number"]
    customer.phone = number

    cardHolder = request.POST["cardHolder"]
    customer.cardHolderr = cardHolder

    cardNo = en.encrypt(request.POST["cardNo"])
    customer.cardNo = cardNo

    cardValidDate = en.encrypt(request.POST["cardValidDate"])
    customer.accountNo = cardValidDate

    customer.save()
    return HttpResponseRedirect("customer_profile")


def updatehp(request):
    return HttpResponse()
