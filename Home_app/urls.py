from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('top_menu_without_sign_in', views.top_menu_without_sign_in),
    path('top_menu_sign_in', views.top_menu_sign_in),
    path('tradie', views.tradie_profile),
    path('tradie_profile', views.tradie_profile),
    path('tradie_current_job', views.tradie_current_job),
    path('tradie_history', views.tradie_history),
    path('about_us', views.about_us),
    path('contact', views.contact),
]

