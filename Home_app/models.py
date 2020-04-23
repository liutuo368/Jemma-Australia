from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_Tradie = models.BooleanField(default=False)
    is_Customer = models.BooleanField(default=False)
    phone = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True)
    suburb = models.CharField(max_length=15)
    state = models.CharField(max_length=5)
    postcode = models.CharField(max_length=5)
    accountStatus = models.CharField(max_length=10)


class Tradie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=50, null=True)
    travelDistance = models.DecimalField(max_digits=4, decimal_places=2)
    ABN = models.CharField(max_length=15)
    BSB = models.CharField(max_length=10)
    accountNo = models.CharField(max_length=10)
    accountName = models.CharField(max_length=30)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cardHolder = models.CharField(max_length=30)
    cardNo = models.CharField(max_length=30)
    cardValidDate = models.CharField(max_length=5)


class Order(models.Model):
    tradie = models.OneToOneField(Tradie, on_delete=models.DO_NOTHING)
    customer = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)
    orderStatus = models.CharField(max_length=15)
    category = models.CharField(max_length=20)
    OrderDate = models.DateTimeField(auto_now_add=True)


class Certificate(models.Model):
    tradie = models.ForeignKey("Tradie", on_delete=models.CASCADE)
    certificateName = models.CharField(max_length=50)
    certificateStatus = models.CharField(max_length=10)
    expireDate = models.DateField()
    price = models.DecimalField(max_digits=4, decimal_places=2)


class Rating(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    order = models.ForeignKey("Order", on_delete=models.DO_NOTHING)
    review = models.CharField(max_length=255)
    points = models.IntegerField()


