from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse


@login_required
def index(request):
    return HttpResponse(
        'Index - Hallo {username} - <a href="/app/logout/">Ausloggen</a>'.format(username=request.user.username)
    )


def app_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next_url']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return HttpResponse('Login failed')
    else:
        next_url = request.GET['next']
        return render(request, 'login.html', {'next_url': next_url})


def app_logout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        print('No User found for logout')
    return redirect(index)


def register(request):
    return HttpResponse('Register')
