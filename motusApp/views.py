from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.template.loader import render_to_string
from django.core import paginator
from django.http import JsonResponse
from datetime import datetime, timedelta
from smtplib import SMTPAuthenticationError
from motusAPI.models import *
from motusApp.decorators import motus_called_from_app
from motusApp.helpers import AddRecordTimeVar, GMail, AddRecordTimeVar, next_record_time_string
from motus.config import lang
import json
import collections


if lang == 'de_DE':
    with open('motusApp/languages/de_DE.json') as file:

        lang = json.load(file)

decorators = [login_required, never_cache]
if settings.DEBUG == False:
    decorators.append(motus_called_from_app)


def app_test(request):

    user = request.user

    today = timezone.now()
    start_date = today - timedelta(days=-1, weeks=1)

    mood_points = 0
    resource_points = 0
    resource_multiplicator = 0.1
    stressor_points = 0
    stressor_multiplicator = 0.05
    possible_mood_points = 3 * 5 * 7 + (0.1 * 5 * 3 * 7)
    
    for dt in date_range(start_date, today):
        records = Record.objects.user_records_for_day(user, dt)
        if records:
            for r in records:

                mood_points += r.mood
                
                resources = r.ressources.all().count()
                if resources < 5:
                    resource_points += resources * resource_multiplicator
                else:
                    resource_points += 5 * resource_multiplicator

                stressors = r.stressors.all().count()
                if stressors < 5:
                    stressor_points += stressors * stressor_multiplicator
                else:
                    stressor_points += 5 * stressor_multiplicator

    total_points = mood_points + resource_points - stressor_points
    score = ((total_points / possible_mood_points) * 100) / 10
                
    print("Mood Points: ", mood_points)
    print("Resource Points: ", resource_points)
    print("Stressor Points: ", stressor_points)
    print("Total Points: ", total_points)
    print("Score: ", score)
    print("")
    print("Possible Mood Points:", 3*5*7)
    print("Possible Resources Points: ", 0.1 * 5 * 3 * 7)
    print("Possible Stressors Points: ", -0.05 * 5 * 3 * 7)

    return HttpResponse("")



def app_version(request):
    return HttpResponse(json.dumps({'version': 140620221423})) 


@method_decorator(decorators, name='dispatch')
class StatisticsView(TemplateView):
    """ Statistics View """

    template_name = 'StatisticPageView.html'

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang

        ressources = []
        for record in self.request.user.records.all():
            for ressource in record.ressources.all():
                ressources.append(ressource)
        context['top5_ressources'] = collections.Counter(ressources).most_common()[0:5]

        stressors = []
        for record in self.request.user.records.all():
            for stressor in record.stressors.all():
                stressors.append(stressor)
        context['top5_stressors'] = collections.Counter(stressors).most_common()[0:5]

        return context


class HelpView(TemplateView):
    """ Help View """        

    template_name = 'HelpPageView.html'

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['lang'] = lang
        return context


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
    records_count_per_page = 5

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.profile_level == 2:

            if user.can_add_record():
                self.can_add_record = True

            if request.GET.get('page'):
                page = int(request.GET.get('page'))
            else:
                page = 1

            records = Record.objects.filter(user=self.request.user).order_by('-id')        
            p = paginator.Paginator(records, self.records_count_per_page)

            try:
                records_page = p.page(page)
            except paginator.EmptyPage:
                records_page = paginator.Page([], page, p)

            if not request.is_ajax():
                context = {
                    'user': user, 
                    'lang': lang, 
                    'records': records_page, 
                    'can_add_record': self.can_add_record, 
                    'next_record': next_record_time_string()
                }
                return render(request, self.template_name, context=context)
            else:
                content = ''
                for record in records_page:
                    content += render_to_string('RecordItemView.html', {'r': record}, request=request)
                return JsonResponse({
                    'content': content,
                    'end_pagination': True if page >= p.num_pages else False
                })

        else:
            return redirect('ProfileLevels')  


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


@method_decorator(decorators, name='dispatch')
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

@login_required
def app_change_resources(request):
    """ Change user resources """
    user = request.user
    return render(
        request, 
        'SetRessourcesView.html', 
        context={
            'user': user, 
            'lang': lang, 
            'ressources': Ressource.objects.all(), 
            'user_ressources': user.ressources.all(),
            'update': True
        }
    )

@login_required
def app_set_ressource(request, id: int):
    """ Activate/Deactivate a ressource for a user profile """
    user = request.user
    ressource = Ressource.objects.get(id=id)

    if user.ressources.filter(id=id).exists():
        user.ressources.remove(ressource)
        return HttpResponse('false')
    else:
        user.ressources.add(ressource)
        return HttpResponse('true')


def date_range(start_date, end_date):
    for n in range(0, int((end_date - start_date).days) + 1, 1):
        yield start_date + timedelta(n)


@login_required
def weekly_data(request):
    """ Return data for weekly chart"""
    user = request.user
    today = timezone.now()
    start_date = today - timedelta(days=-1, weeks=1)

    days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    moodValues = [-2, -1, 0, 1, 2]
    data = [[],[]]
    
    for dt in date_range(start_date, today):
        records = Record.objects.user_records_for_day(user, dt)
        data[0].append(days[dt.weekday()])
        if records:
            average = 0
            for r in records:
                average += moodValues[r.mood-1]
            average /= len(records)
            data[1].append(average)
        else:
            data[1].append(None)

    return HttpResponse(json.dumps(data))


@login_required
def alltime_data(request):
    """ Return data for alltime chart """
    user = request.user
    records = Record.objects.user_records(user)
    data = [0, 0, 0, 0, 0]
    for r in records: 
        data[r.mood-1] += 1

    return HttpResponse(json.dumps(data))
