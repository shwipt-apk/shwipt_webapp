from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user_clubs/', views.get_user_club),
    path('joined_clubs/', views.get_joined_club),
    path('explore_clubs/', views.get_explore_club),
    path('join_clubs/', views.post_join_club),
    path('create_clubs/', views.post_create_club),
    path('club_posts/', views.get_club_post),
    path('club_members/', views.get_club_members),
    path('club_interests/', views.get_club_interests),
    path('message_reacts/', views.get_message_reacts),
    path('react_exists/', views.get_react_exists),
    path('like_post/', views.get_post_likes),
    path('post_comment/', views.get_post_comments),
    path('like_list/', views.post_feed_likes),
    path('comment_list/', views.post_feed_comments),
    path('edit_club/', views.put_edit_club)
]
