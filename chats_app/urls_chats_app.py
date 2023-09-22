from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('chat_history/', views.get_chat_history)
]