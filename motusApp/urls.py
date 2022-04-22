from django.urls import path
from motusApp.views import app_login, app_logout, app_register, app_index, app_profile, app_activate_profile


urlpatterns = [
    path(
        '',
        app_index,
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
        app_register,
        name='register'
    ),
    path(
        'profile/',
        app_profile,
        name='profile'
    ),
    path(
        'activate/<activation_code>/',
        app_activate_profile,
        name='activate_profile'
    ),
]
