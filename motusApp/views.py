from django.shortcuts import render
from django.http import HttpResponse


def app_login(request):
    return render(request, 'app/login.html')
