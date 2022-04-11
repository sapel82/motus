from django.urls import path
from django.views.generic import RedirectView
from motusAPI.views import api_startpage, api_profile_call, api_gender_call
from motus.config import motus_api_version

urlpatterns = [
    path(
        '',
        RedirectView.as_view(url='{version}/'.format(version=motus_api_version)),
        name='Index'
    ),
    path(
        '{version}/'.format(version=motus_api_version),
        api_startpage,
        name='API Startpage'
    ),
    path(
        '{version}/profile/<profile_id>/'.format(version=motus_api_version),
        api_profile_call,
        name='API profile call with id'
    ),
    path(
        '{version}/profile/'.format(version=motus_api_version),
        api_profile_call,
        name='API profile call without id'
    ),
    path(
        '{version}/gender/<gender_id>/'.format(version=motus_api_version),
        api_gender_call,
        name='API gender call with id'
    ),
    path(
        '{version}/gender/'.format(version=motus_api_version),
        api_gender_call,
        name='API gender call without id'
    ),
]
