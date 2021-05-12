from django.urls import path

from .views import Custom_Login, Custom_SignUp


from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup', Custom_SignUp.as_view(), name='signup'),
    path('login',Custom_Login.as_view(), name='login'),
    path('login/refresh',TokenRefreshView.as_view(), name='refesh')
]