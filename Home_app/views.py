from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.hashers import make_password

from Home_app.models import Tradie
from Home_app.models import Customer
from Home_app.models import Order
from Home_app.models import TradieJobType
from Home_app.models import Rating
from Home_app.models import MyUser
from Home_app.models import Quote
from Home_app.models import QuoteImage
from django.db.models import Q
import json
import Jemma.Encrypt as en
from Jemma.settings import BASE_DIR


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
        if user_type == "Tradie":
            try:
                Tradie.objects.get(myUser=user)
                auth.login(request, user)
                return HttpResponseRedirect("tradie")
            except Tradie.DoesNotExist:
                raise Http404("Tradie does not exist")
        elif user_type == "Customer":
            try:
                Customer.objects.get(myUser=user)
                auth.login(request, user)
                return HttpResponseRedirect("customer")
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
        myUser = MyUser(email=email, date_of_birth='2020-1-1', user_type=user_type, password=make_password(password))
        myUser.save()
        if user_type == "Tradie":
            tradie = Tradie(myUser=myUser, first_name=firstname, last_name=lastname, accountStatus="Active", travelDistance=0)
            tradie.save()
            auth.login(request, myUser)
            return HttpResponseRedirect("tradie")
        else:
            customer = Customer(myUser=myUser, first_name=firstname, last_name=lastname, accountStatus="Active")
            customer.save()
            auth.login(request, myUser)
            return HttpResponseRedirect("customer_profile")


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
            "job_history": job_history,
            "fullname": tradie.first_name + " " + tradie.last_name
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
            "current_jobs": current_jobs,
            "fullname": tradie.first_name + " " + tradie.last_name
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
    job_list = TradieJobType.objects.filter(tradie=tradie)
    avg_rating = 5
    if len(rating_list) > 0:
        sum_rating = 0
        for rating in rating_list:
            sum_rating += rating.points
        avg_rating = round(sum_rating / len(rating_list), 1)
    context = {
        "tradie": tradie,
        "rating_number": len(rating_list),
        "rating": avg_rating,
        "rating_list": rating_list,
        "job_list": job_list
    }
    return render(request, "Customer/tradie_detail.html", context)


def send_quote(request):
    tradie_id = request.POST["tradie_id"]
    description = request.POST["description"]
    images = request.FILES.getlist("files[]")
    quote = Quote(customer=(Customer.objects.get(myUser=request.user)), tradie=(Tradie.objects.get(myUser_id=tradie_id)), description=description)
    quote.save()
    for img in images:
        image = QuoteImage(image=img, quote=quote)
        image.save()
    return HttpResponseRedirect("tradie_detail?tradie_id=" + tradie_id)


def tradie_calendar(request):
    return render(request, "Tradie/tradie_calendar.html")

def tradie_quotes(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        current_quotes = Quote.objects.filter(Q(tradie=tradie))
        context = {
            "login_status": json.dumps(True),
            "current_quotes": current_quotes,
            "fullname": tradie.first_name + " " + tradie.last_name
        }
        return render(request, "Tradie/tradie_quotes.html", context)
    else:
        raise Http404("Haven't logged in")


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

def customer_quote(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Customer does not exist")
        current_quotes = Quote.objects.filter(Q(customer=customer))
        context = {
            "login_status": json.dumps(True),
            "current_quotes": current_quotes,
            "fullname": customer.first_name + " " + customer.last_name
        }
        return render(request, "Customer/customer_quote.html", context)
    else:
        raise Http404("Haven't logged in")


def customer_history(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(myUser=request.user)
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")
        order_history = Order.objects.filter(Q(customer=customer), Q(orderStatus="Rejected") | Q(orderStatus="Completed"))
        context = {
            "login_status": json.dumps(True),
            "order_history": order_history,
            "fullname": customer.first_name + " " + customer.last_name
        }
        return render(request, "Customer/customer_history.html", context)
    else:
        raise Http404("Haven't logged in")


def customer_current_order(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(myUser=request.user)
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")
        current_offers = Order.objects.filter(Q(customer=customer), Q(orderStatus="Pending") | Q(orderStatus="Accepted"))
        context = {
            "login_status": json.dumps(True),
            "current_orders": current_offers,
            "fullname": customer.first_name + " " + customer.last_name
        }
        return render(request, "Customer/customer_current_order.html", context)
    else:
        raise Http404("Haven't logged in")


def tradie_quote_details(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        quote_id = request.GET["quote_id"]
        current_quote = Quote.objects.get(id=quote_id)
        images = QuoteImage.objects.filter(quote=current_quote)
        context = {
            "login_status": json.dumps(True),
            "current_quote": current_quote,
            "fullname": tradie.first_name + " " + tradie.last_name,
            "images": images
        }
        return render(request, "Tradie/tradie_quote_details.html", context)
    else:
        raise Http404("Haven't logged in")


def tradie_accept_quote(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        quote_id = request.POST["quote_id"]
        price = request.POST["price"]
        current_quote = Quote.objects.get(id=quote_id)
        if current_quote.tradie == tradie:
            current_quote.status = "Responded"
            current_quote.price = float(price)
            current_quote.save()
            return HttpResponseRedirect("tradie_quote_details?quote_id=" + quote_id)
        else:
            raise Http404("You don't have permission to do that")
    else:
        raise Http404("Haven't logged in")


def tradie_decline_quote(request):
    if request.user.is_authenticated:
        try:
            tradie = Tradie.objects.get(myUser=request.user)
        except Tradie.DoesNotExist:
            raise Http404("Tradie does not exist")
        quote_id = request.GET["id"]
        current_quote = Quote.objects.get(id=quote_id)
        if current_quote.tradie == tradie:
            current_quote.status = "Declined"
            current_quote.save()
            return HttpResponseRedirect("tradie_quote_details?quote_id=" + quote_id)
        else:
            raise Http404("You don't have permission to do that")
    else:
        raise Http404("Haven't logged in")


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

    cardHolder = en.encrypt(request.POST["cardHolder"])
    customer.cardHolder = cardHolder

    cardNo = en.encrypt(request.POST["cardNumber"])
    customer.cardNo = cardNo

    cardValidDate = en.encrypt(request.POST["cardValidDate"])
    customer.cardValidDate = cardValidDate

    customer.save()
    return HttpResponseRedirect("customer_profile")


def updatehp(request):
    return HttpResponse()
