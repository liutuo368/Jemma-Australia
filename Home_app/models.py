from django.db import models


# Create your models here.
class Tradie(models.Model):
    TradieId = models.CharField(max_length=10, primary_key=True)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Pass = models.CharField(max_length=20)
    Email = models.EmailField
    Phone = models.CharField(max_length=10)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100, null=True)
    Suburb = models.CharField(max_length=15)
    State = models.CharField(max_length=5)
    Postcode = models.CharField(max_length=5)
    Company = models.CharField(max_length=50, null=True)
    TravelDistance = models.DecimalField
    ABN = models.CharField(max_length=15)
    BSB = models.CharField(max_length=10)
    AccountNo = models.CharField(max_length=10)
    AccountName = models.CharField(max_length=30)
    AccountStatus = models.CharField(max_length=10)


class Customer(models.Model):
    CustomerId = models.CharField(max_length=10, primary_key=True)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Pass = models.CharField(max_length=20)
    Email = models.EmailField
    Phone = models.CharField(max_length=10)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100, null=True)
    Suburb = models.CharField(max_length=15)
    State = models.CharField(max_length=5)
    Postcode = models.CharField(max_length=5)
    CardHolder = models.CharField(max_length=30)
    CardNo = models.CharField(max_length=30)
    CardValidDate = models.CharField(max_length=5)
    AccountStatus = models.CharField(max_length=10)


class Order(models.Model):
    OrderId = models.CharField(max_length=10, primary_key=True)
    OrderStatus = models.CharField(max_length=15)
    Category = models.CharField(max_length=20)
    OrderDate = models.DateField
    TradieId = models.ForeignKey(Tradie, on_delete=models.CASCADE)
    CustomerId = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Certificate(models.Model):
    TradieId = models.ForeignKey(Tradie, on_delete=models.CASCADE)
    CertificateName = models.CharField(max_length=50)
    CertificateStatus = models.CharField(max_length=10)
    ExpireDate = models.DateField
    Price = models.DecimalField

    class Meta:
        unique_together = ("TradieId", "CertificateName")


class Rating(models.Model):
    UserId = models.CharField(max_length=10)
    OrderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    Review = models.CharField(max_length=255)
    Points = models.IntegerField

    class Meta:
        unique_together = ("UserId", "OrderId")

