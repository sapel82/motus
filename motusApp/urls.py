from django.urls import path
from motusApp.views import app_login, register, index


urlpatterns = [
    path(
        '',
        index,
        name='index'
    ),
    path(
        'login/',
        app_login,
        name='login'
    ),
    path(
        'register/',
        register,
        name='register'
    ),

]
