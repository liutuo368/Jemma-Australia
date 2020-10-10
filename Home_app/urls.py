from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login', views.login),
    path('user_logout', views.user_logout),
    path('terms_and_conditions', views.terms_and_conditions),
    path('top_menu_without_sign_in', views.top_menu_without_sign_in),
    path('top_menu_sign_in', views.top_menu_sign_in),
    path('footer', views.footer),
    path('side_menu', views.side_menu),
    path('tradie', views.tradie_profile),
    path('profile', views.profile),
    path('tradie_profile', views.tradie_profile),
    path('tradie_current_job', views.tradie_current_job),
    path('tradie_history', views.tradie_history),
    path('tradie_calendar', views.tradie_calendar),
    path('about_us', views.about_us),
    path('contact', views.contact),
    path('update_tradie_profile', views.update_tradie_profile),
    path('customer_search_result', views.customer_search_result),
    path('tradie_detail', views.tradie_detail),
    path('sign_up', views.sign_up),
    path('side_menu_customer', views.side_menu_customer),
    path('tradie_quotes', views.tradie_quotes),
    path('customer_profile', views.customer_profile),
    path('customer', views.customer_profile),
    path('customer_quote', views.customer_quote),
    path('customer_history', views.customer_history),
    path('customer_current_order', views.customer_current_order),
    path('tradie_quote_details', views.tradie_quote_details),
    path('customer_quote_details', views.customer_quote_details),
    path('update_customer_profile', views.update_customer_profile),
    path('send_quote', views.send_quote),
    path('accept_quote', views.tradie_accept_quote),
    path('decline_quote', views.tradie_decline_quote),
    path('customer_decline_quote', views.customer_decline_quote),
    path('tradie_order_detail', views.tradie_order_detail),
    path('customer_finish_payment', views.customer_finish_payment),
    path('tradie_finish_job', views.tradie_finish_job),
    path('upload_hp', views.upload_hp),
    path('customer_order_detail', views.customer_order_detail),
    path('tradie_rating', views.tradie_rating),
    path('customer_rating', views.customer_rating),
    path('not_found', views.not_found),
    path('not_login_error', views.not_login_error),
    path('wrong_account_error', views.wrong_account_error)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)