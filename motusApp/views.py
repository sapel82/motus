from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from smtplib import SMTPAuthenticationError
from motusAPI.models import Gender, User
from motusApp.helpers import GMail


@login_required
def app_index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'user': request.user})
    else:
        return HttpResponse('user not found')


@login_required
def app_profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        return HttpResponse('user not found')


def app_activate_profile(request, activation_code: int):
    alerts = []
    if User.objects.filter(activation_code=activation_code).exists():
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.save()
    else:
        alerts.append('Für diesen Aktivierungscode wurde kein Benutzer gefunden.')
    return render(request, 'activation_done.html', {'alerts': alerts})


def app_login(request):
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
            alerts.append(
                '''
                <p>Login fehlgeschlagen!</p>  
                <p>Was kannst du tun?</p>
                <p>1. Bitte überprüfe Benutzername und Passwort.</p>
                <p>2. Vergewissere dich, dass du den Bestätigungslink in deiner Email angeklickt hast.</p>
                '''
            )
            return render(request, 'login.html', {'next_url': next_url, 'alerts': alerts})
    else:
        next_url = request.GET['next']
        return render(request, 'login.html', {'next_url': next_url})


def app_logout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        print('No User found for logout')
    return redirect(app_index)


def app_register(request):
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
                alerts.append('Der Benutzername ist schon vergeben, bitte wähle einen anderen.')
            if User.objects.filter(email=email).exists():
                alerts.append('Die E-Mail Adresse ist schon vergeben, bitte wähle eine andere.')
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
                        subject = 'Willkommen bei motus - Bestätigungsmail'
                        message = 'Hallo {username},\num deinen Account zu aktivieren, klicke bitte auf den folgenden' \
                                  ' Link:\n\nhttp://78.47.48.92:8000/app/activate/{activation_code}/'.format(
                                                                                username=user.username,
                                                                                activation_code=user.activation_code)
                        mail.send([email], subject, message)
                    except SMTPAuthenticationError as e:
                        alerts.append('Die Bestätigungsmail konnte nicht gesendet werden.')
                else:
                    alerts.append('Der Benutzer konnte nicht erstellt werden.')
        else:
            alerts.append("Es fehlen wichtige Nutzerdaten.")

        return render(request, 'after_register.html', {'alerts': alerts, 'user': user})
    else:
        return render(request, 'register.html')
