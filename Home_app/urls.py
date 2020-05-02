from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login', views.login),
    path('top_menu_without_sign_in', views.top_menu_without_sign_in),
    path('top_menu_sign_in', views.top_menu_sign_in),
    path('footer', views.footer),
    path('side_menu', views.side_menu),
    path('tradie', views.tradie_profile),
    path('tradie_profile', views.tradie_profile),
    path('tradie_current_job', views.tradie_current_job),
    path('tradie_history', views.tradie_history),
    path('tradie_calendar', views.tradie_calendar),
    path('about_us', views.about_us),
    path('contact', views.contact),
    path('updatehp/', views.updatehp),
]

