from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from smtplib import SMTPAuthenticationError
from motusAPI.models import *
from motusApp.helpers import GMail
from motus.config import lang
import json

if lang == 'de_DE':
    with open('motusApp/languages/de_DE.json') as file:
        lang = json.load(file)


def app_test(request):
    return HttpResponse('test')


@login_required
def app_index(request):
    """ Mainpage """
    user = request.user
    if user.is_authenticated:
        if user.profile_level == 2:
            records = Record.objects.all()
            records_today = Record.objects.get

            ts = datetime.now()
            print(ts)


            return render(
                request, 
                'index.html', 
                {
                    'user': user, 
                    'lang': lang,
                    'records': records,
                }
            )
        else:
            return redirect(app_fill_profile)


@login_required
def app_fill_profile(request):
    """ Check Profile Status """
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_profile_level = request.POST['new_profile_level']
            request.user.profile_level = new_profile_level
            request.user.save()
            return redirect(app_index)
        else:
            if request.user.profile_level == 0:
                return render(request, 'profile_info.html', {'user': request.user, 'lang': lang})
            elif request.user.profile_level == 1:
                ressources = Ressource.objects.all()
                return render(
                    request, 'profile_set_ressources.html', {
                        'user': request.user,
                        'lang': lang,
                        'user_ressources': request.user.ressources.all(),
                        'ressources': ressources
                    }
                )
            elif request.user.profile_level == 2:
                return redirect(app_index)


@login_required
def app_profile(request):
    """ Profile Page """
    if request.user.is_authenticated:
        ressources = Ressource.objects.all()
        return render(
            request, 
            'profile.html',
            {
                'user': request.user, 
                'lang': lang, 
                'ressources': ressources,
                'user_ressources': request.user.ressources.all()}
        )


def app_activate_profile(request, activation_code: int):
    """ Activation Page """
    alerts = []
    if User.objects.filter(activation_code=activation_code).exists():
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.save()
    else:
        alerts.append(lang['ERROR_ACTIVATION_CODE_NOT_FOUND'])
    return render(request, 'activation_done.html', {'alerts': alerts, 'lang': lang})


def app_set_ressource(request, id: int):
    """ Activate/Deactivate a ressource for a user profile """
    user =request.user
    ressource = Ressource.objects.get(id=id)

    if user.ressources.filter(id=id).exists():
        user.ressources.remove(ressource)
        return HttpResponse('false')
    else:
        user.ressources.add(ressource)
        return HttpResponse('true')
      

def app_login(request):
    """ Login Page """
    if request.method == 'POST':
        alerts = []
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next_url']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            alerts.append(lang['ERROR_LOGIN_FAILED'])
            return render(request, 'login.html', {'next_url': next_url, 'alerts': alerts, 'lang': lang})
    else:
        next_url = request.GET['next']
        return render(request, 'login.html', {'next_url': next_url, 'lang': lang})


def app_logout(request):
    """ Logout """
    if request.user.is_authenticated:
        logout(request)
    else:
        print(lang['ERROR_LOGOUT_FAILED'])
    return redirect(app_index)


def app_register(request):
    """ Registration Page """
    if request.method == 'POST':

        alerts = []
        user = None

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        date_of_birth = datetime.strptime(request.POST['dateOfBirth'], '%Y-%m-%d')
        gender = Gender.objects.get(title=request.POST['gender'])

        if all([username, email, password, date_of_birth, gender]):
            if User.objects.filter(username=username).exists():
                alerts.append(lang['ERROR_USERNAME_NOT_AVAILABLE'])
            if User.objects.filter(email=email).exists():
                alerts.append(lang['ERROR_EMAIL_NOT_AVAILABLE'])
            if len(alerts) == 0:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    password=password
                )

                if user:
                    try:
                        mail = GMail()
                        subject = lang['MAIL_REGISTER_SUBJECT']
                        msg = lang['MAIL_REGISTER_MSG'].format(username=username, activation_code=user.activation_code)
                        mail.send([email], subject, msg)
                    except SMTPAuthenticationError as e:
                        alerts.append(lang['ERROR_EMAIL_NOT_SEND'])
                else:
                    alerts.append(lang['ERROR_USER_NOT_CREATED'])
        else:
            alerts.append(lang['ERROR_MISSING_USERDATA'])

        return render(request, 'after_register.html', {'alerts': alerts, 'user': user, 'lang': lang})
    else:
        return render(request, 'register.html', {'lang': lang})
