from django.urls import path
from motusApp.views import app_login, app_logout, register, index


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
        'logout/',
        app_logout,
        name='logout'
    ),
    path(
        'register/',
        register,
        name='register'
    ),

]
