from django.urls import path

from .views import Custom_SignUp, Custom_Login, Custom_Logout

urlpatterns = [
    path('signup', Custom_SignUp.as_view(), name='signup'),
    path('login',Custom_Login.as_view(), name='login'),
    path('logout',Custom_Logout.as_view(), name='logout')
]