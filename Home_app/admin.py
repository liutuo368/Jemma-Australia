from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

register_list = [
    models.Tradie,
    models.Customer,
    models.Order,
    models.Certificate,
    models.Rating
]

admin.site.register(register_list)

