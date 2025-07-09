from django.urls import path
from django.contrib.auth import views as auth_view
from .views import check_auth, firstinit, LoginOrRegisterView 

urlpatterns = [
    path('login/', LoginOrRegisterView.as_view(next_page='dashboard'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('auth-check/', check_auth, name='auth_check'),
    path('firstinit', firstinit, name='firstinit'),
]