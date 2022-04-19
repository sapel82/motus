from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


@login_required
def index(request):
    return HttpResponse("Index")


def app_login(request):
    return render(request, 'login.html')


def register(request):
    return HttpResponse('Register')
