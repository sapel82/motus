from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from datetime import datetime
from smtplib import SMTPAuthenticationError
from motusAPI.models import *
from motusApp.helpers import AddRecordTimeVar, GMail, AddRecordTimeVar
from motus.config import lang
import json


if lang == 'de_DE':
    with open('motusApp/languages/de_DE.json') as file:
        lang = json.load(file)

decorators = [login_required, never_cache]


def app_test(request):
    return HttpResponse('test')


@method_decorator(decorators, name='dispatch')
class AddRecordView(TemplateView):
    """ Add Record View """

    template_name = 'AddRecordView.html'

    def get(self, request):
        user = request.user
        if user.can_add_record():
            return render(request, self.template_name, context=self.get_context_data())
        else:
            return redirect('MainPage')

    def post(self, request):

        now = timezone.now()
        mood = request.POST['mood']
        note = request.POST['note']

        r = Record(timestamp=now, mood=mood, note=note)
        r.save()
        request.user.records.add(r)

        ressources_count = Ressource.objects.all().count()
        stressor_count = Stressor.objects.all().count()

        for i in range(1, ressources_count + 1):
            if 'r_{id}'.format(id=i) in request.POST:
                r.ressources.add(Ressource.objects.filter(id=i).first())

        for i in range(1, stressor_count + 1):
            if 's_{id}'.format(id=i) in request.POST:
                r.stressors.add(Stressor.objects.filter(id=i).first())

        return redirect('MainPage')

    def get_context_data(self, **kwargs):
        lang['ADD_RECORD_RESSOURCE_QUESTION'] = lang['ADD_RECORD_RESSOURCE_QUESTION'].format(time=AddRecordTimeVar())
        lang['ADD_RECORD_STRESSOR_QUESTION'] = lang['ADD_RECORD_STRESSOR_QUESTION'].format(time=AddRecordTimeVar())
        print(lang['ADD_RECORD_STRESSOR_QUESTION'])        
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        context['ressources'] = Ressource.objects.all()
        context['stressors'] = Stressor.objects.all()
        return context


@method_decorator(decorators, name='dispatch')
class MainPageView(TemplateView):
    """ Main Page """

    template_name = 'MainPage.html'
    can_add_record = False

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.profile_level == 2:
            if user.can_add_record():
                self.can_add_record = True
            return render(request, self.template_name, context=self.get_context_data())
        else:
            return redirect('ProfileLevels')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        context['can_add_record'] = self.can_add_record
        context['records'] = Record.objects.filter(user=self.request.user).order_by('-id')
        return context


@method_decorator(decorators, name='dispatch')
class ProfileLevelsView(TemplateView):
    """ Various Profile Levels Views """

    profile_info_template_name = 'ProfileInfoView.html'
    profile_set_ressources_template_name = 'SetRessourcesView.html'

    def get(self, request):
        user = request.user
        if user.profile_level == 0:
            return render(request, self.profile_info_template_name, context=self.get_context_data())
        elif request.user.profile_level == 1:
            return render(request, self.profile_set_ressources_template_name, context=self.get_context_data())
        elif request.user.profile_level == 2:
            return redirect('MainPage')

    def post(self, request):
        user = request.user
        new_profile_level = request.POST['new_profile_level']
        user.profile_level = new_profile_level
        user.save()
        return redirect('MainPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        context['ressources'] = Ressource.objects.all()
        context['user_ressources'] = self.request.user.ressources.all()
        return context


class ProfileView(TemplateView):
    """ Profile View """

    template_name = 'ProfileView.html'

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['user'] = self.request.user
        context['lang'] = lang
        context['user_ressources'] = self.request.user.ressources.all()
        return context
        

class ActivateProfileView(TemplateView):
    """ Activation Profile View """

    template_name = 'ActivateProfileView.html'
    alerts = []

    def get(self, request, activation_code: int):
        if User.objects.filter(activation_code=activation_code).exists():
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.save()
        else:
            self.alerts.append(lang['ERROR_ACTIVATION_CODE_NOT_FOUND'])
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        context['alerts'] = self.alerts
        return context
      

class LoginView(TemplateView):
    """ Login Page """

    template_name = 'LoginView.html'
    alerts = []
    next_url = ''

    def get(self, request, *args, **kwargs):
        self.alerts.clear()
        self.next_url = request.GET['next']
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        self.next_url = request.POST['next_url']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(self.next_url)
        else:
            self.alerts.append(lang['ERROR_LOGIN_FAILED'])
            return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        context['next_url'] = self.next_url
        context['alerts'] = self.alerts
        return context


class LogoutView(View):
    """ Logout View """

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return redirect('MainPage')
        else:
            return HttpResponse(lang['ERROR_LOGOUT_FAILED'])


class RegistrationView(TemplateView):
    """ Registration Views """

    register_template_name = 'RegisterView.html'
    register_done_template_name = 'RegisterDoneView.html'

    alerts = []
    user = None

    def get(self, request):
        return render(request, self.register_template_name, context=self.get_context_data())

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        date_of_birth = datetime.strptime(request.POST['dateOfBirth'], '%Y-%m-%d')
        gender = Gender.objects.get(title=request.POST['gender'])

        if all([username, email, password, date_of_birth, gender]):
            if User.objects.filter(username=username).exists():
                self.alerts.append(lang['ERROR_USERNAME_NOT_AVAILABLE'])
            if User.objects.filter(email=email).exists():
                self.alerts.append(lang['ERROR_EMAIL_NOT_AVAILABLE'])
            if len(self.alerts) == 0:
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
                        self.alerts.append(lang['ERROR_EMAIL_NOT_SEND'])
                else:
                    self.alerts.append(lang['ERROR_USER_NOT_CREATED'])
        else:
            self.alerts.append(lang['ERROR_MISSING_USERDATA'])

        return render(request, self.register_done_template_name, context=self.get_context_data())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        return context


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
