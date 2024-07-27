from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('api/register1/', views.register_api, name='api-register'),
    path('api/login1/', views.api_login_view, name='api-login'),
    path('api/profile1/', views.api_profile_view, name='api-profile'),
    path('api/logout1/', views.api_logout_view, name='api-logout'),
]