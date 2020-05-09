from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from enum import Enum


class UserTypeChoice(Enum):
    Tradie = "Tradie"
    Customer = "Customer"

class OrderStatusTypeChoice(Enum):
    Accepted = "Accepted"
    Pending = "Pending"
    Rejected ="Rejected"
    Completed ="Completed"


### BEGIN DEFINE MYUSER ###

# Modified from Official Example
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, user_type, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password = password,
            date_of_birth = date_of_birth,
            user_type='SuperUser'
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Modified from Official Example
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    user_type = models.CharField(
        null=True,
        max_length=10,
        choices=[(_type.name, _type.value) for _type in UserTypeChoice],
        default='Customer'
    )

    user_hp = models.ImageField(upload_to='user_hp', default='default_hp.png')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest #possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

### END DEFINE MYUSER ###


class Tradie(models.Model):
    myUser = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    suburb = models.CharField(max_length=15)
    state = models.CharField(max_length=5)
    postcode = models.CharField(max_length=5)
    company = models.CharField(max_length=50, null=True, blank=True)
    travelDistance = models.DecimalField(max_digits=4, decimal_places=2)
    ABN = models.CharField(max_length=15)
    BSB = models.CharField(max_length=10)
    accountNo = models.CharField(max_length=10)
    accountName = models.CharField(max_length=30)
    accountStatus = models.CharField(max_length=10)


class Customer(models.Model):
    myUser = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    suburb = models.CharField(max_length=15)
    state = models.CharField(max_length=5)
    postcode = models.CharField(max_length=5)
    cardHolder = models.CharField(max_length=30)
    cardNo = models.CharField(max_length=30)
    cardValidDate = models.CharField(max_length=5)
    accountStatus = models.CharField(max_length=10)


class Order(models.Model):
    orderStatus = models.CharField(
        null=True,
        max_length=15,
        choices=[(_type.name, _type.value) for _type in OrderStatusTypeChoice],
        default='Pending')
    category = models.CharField(max_length=20)
    tradie = models.ForeignKey("Tradie", on_delete=models.CASCADE)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    orderDate = models.DateTimeField(auto_now_add=True)


class Certificate(models.Model):
    tradie = models.ForeignKey("Tradie", on_delete=models.CASCADE)
    certificateName = models.CharField(max_length=50)
    certificateStatus = models.CharField(max_length=10)
    expireDate = models.DateField()
    price = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ("tradie", "certificateName")


class Rating(models.Model):
    user = models.ForeignKey("MyUser", on_delete=models.DO_NOTHING)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    points = models.IntegerField()

    class Meta:
        unique_together = ("user", "order")

