from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('tradie', views.tradie_profile),
    path('tradie_profile', views.tradie_profile),
    path('tradie_current_job', views.tradie_current_job),
    path('tradie_history', views.tradie_history),
    path('about_us', views.about_us),
    path('contact', views.contact),
]

