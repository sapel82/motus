from django.urls import path
from motusApp.views import app_login


urlpatterns = [
    path(
        '',
        app_login,
        name='App - Login'
    ),

]
