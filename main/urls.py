# main/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('follow/<uuid:pk>/', views.follow_user, name='follow_user'),
    path('unfollow/<uuid:pk>/', views.unfollow_user, name='unfollow_user'),
    path('profile/<uuid:pk>/', views.user_profile, name='user_profile'),
    path('like/<uuid:pk>/', views.like_post, name='like_post'),
    path('comment/<uuid:pk>/', views.comment_post, name='comment_post'),
    path('delete_comment/<uuid:pk>/', views.delete_comment, name='delete_comment'),
    path('search/', views.user_search, name='user_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)