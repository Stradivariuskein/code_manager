from django.urls import path
from django.contrib.auth import views as auth_view
from .views import check_auth

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', auth_view.LoginView.as_view(), name='logout'),
    path('auth-check/', check_auth, name='auth_check'),
]