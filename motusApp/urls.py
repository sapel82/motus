from django.urls import path
from motusApp.views import *


urlpatterns = [
    path(
        '',
        MainPageView.as_view(),
        name = 'MainPage'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='Login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='Logout'
    ),
    path(
        'register/',
        RegistrationView.as_view(),
        name='Registration'
    ),
    path(
        'profile/',
        ProfileView.as_view(),
        name='Profile'
    ),
    path(
        'fill_profile/',
        ProfileLevelsView.as_view(),
        name='ProfileLevels'
    ),
    path(
        'activate/<activation_code>/',
        ActivateProfileView.as_view(),
        name='ActivateProfile'
    ),
    path(
        'set/ressource/<id>/',
        app_set_ressource,
        name='set_ressource'
    ),
    path(
        'add_record/',
        AddRecordView.as_view(),
        name='AddRecord'
    ),
    path(
        'test/',
        app_test,
        name='test'
    )
]
