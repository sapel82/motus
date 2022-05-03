from django.urls import path
from motusApp.views import *


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
        'fill_profile/',
        app_fill_profile,
        name='fill_profile'
    ),
    path(
        'activate/<activation_code>/',
        app_activate_profile,
        name='activate_profile'
    ),
    path(
        'set/ressource/<id>/',
        app_set_ressource,
        name='set_ressource'
    ),
    path(
        'test/',
        app_test,
        name='test'
    )
]
