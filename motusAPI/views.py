import json
from django.http import HttpResponse
from django.core import serializers
from motus.config import motus_api_version, motus_api_name
from motusAPI.models import User, Gender


def api_startpage(request) -> HttpResponse:
    return HttpResponse('''
        <h1>{name} Version {version}</h1>
        <h2>API for Motus: Emotion Tracking App (Android)</h2>
    '''.format(name=motus_api_name, version=motus_api_version))


def api_profile_call(request, profile_id: int = None) -> HttpResponse:
    if profile_id:
        data = serializers.serialize('json', User.objects.filter(id=profile_id))
    else:
        data = serializers.serialize('json', User.objects.all())
    return HttpResponse(data, content_type='json')


def api_gender_call(request, gender_id: int = None) -> HttpResponse:
    if gender_id:
        data = serializers.serialize('json', Gender.objects.filter(id=gender_id))
    else:
        data = serializers.serialize('json', Gender.objects.all())
    return HttpResponse(data, content_type='json')
