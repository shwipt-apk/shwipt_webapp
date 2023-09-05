from django.contrib import admin
from django.urls import path,include
from users_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users_app.urls_users_app')),
    path('clubs/', include('clubs_app.urls_clubs_app')),
    path('feeds/', include('feeds_app.urls_feeds_app')),
    path('chats/', include('chats_app.urls_chats_app')),
    path('settings/', include('settings_app.urls_settings_app')),
    path('payments/', include('payments_app.urls_payments_app')),
    path('notifications/', include('notifications_app.urls_notifications_app')),
    path('superAdmin/', include('admin_app.urls_admin_app')),
]
