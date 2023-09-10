from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('users_info/', views.get_user),
    path('edit_profile/', views.put_edit_userProfile),
    path('edit_social/', views.put_edit_userSocial),
    path('active_users/', views.get_active_user),
    path('active_friends/', views.get_active_friends),
    path('alltime_popular/', views.get_alltime_popular),
    path('weekly_popular/', views.get_weekly_popular),
    path('create_user/', views.post_create_user),
    path('user_posts/', views.get_user_post),
    path('sent_requests/', views.post_user_request),
    path('request_accepted/', views.post_request_accept),
    path('request_rejected/', views.post_request_reject),
    path('cancel_requests/', views.put_cancel_request),
    path('user_connection/', views.get_user_connection),
    path('user_report/', views.post_user_report),
    path('user_block/', views.post_user_block),
    path('user_unfriend/', views.put_user_unfriend),
    path('user_connections/', views.get_friends),
    path('email_exists/', views.get_email_existence),
    path('username_exists/', views.get_username_existence),
    path('phone_exists/', views.get_phone_existence),
]
