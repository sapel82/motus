import smtplib
import ssl
from django.utils import timezone
import json

from motus.config import lang
from motus.config import EMAIL_SENDER, EMAIL_PORT, EMAIL_SMTP_SERER_DOMAIN, EMAIL_PASSWORD

if lang == 'de_DE':
    with open('motusApp/languages/de_DE.json') as file:
        lang = json.load(file)


class GMail:

    def __init__(self):
        self.port = EMAIL_PORT
        self.smtp_server_domain_name = EMAIL_SMTP_SERER_DOMAIN
        self.sender_mail = EMAIL_SENDER
        self.password = EMAIL_PASSWORD

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}".encode('utf-8'))

        service.quit()


def AddRecordTimeVar():
    now = timezone.now()
    if now.hour >= 0 and now.hour < 12:
        return lang['ADD_RECORD_MORNING_VAR']
    if now.hour >= 12 and now.hour < 18:
        return lang['ADD_RECORD_NOON_VAR']
    if now.hour >= 18 and now.hour < 24:
        return lang['ADD_RECORD_EVENING_VAR']


def next_record_time_string():
    ts = timezone.now()
    if ts.hour >= 0 and ts.hour < 12:
        possible = ts.replace(hour=12, minute=0, second=0) - ts
    elif ts.hour >= 12 and ts.hour < 18:
        possible = ts.replace(hour=18, minute=0, second=0) - ts
    elif ts.hour >= 18 and ts.hour < 24:
        possible = ts.replace(hour=0, minute=0, second=0) - ts

    possible_seconds = possible.seconds
    hours, remainder = divmod(possible_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if int(hours) == 0:
        if int(minutes) == 1:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_1'].format(minutes=int(minutes))
        else:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_2'].format(minutes=int(minutes))
    elif int(hours) == 1:
        if int(minutes) == 1:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_3'].format(hours=int(hours), minutes=int(minutes))
        else:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_4'].format(hours=int(hours), minutes=int(minutes))
    else:
        if int(minutes) == 1:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_5'].format(hours=int(hours), minutes=int(minutes))
        else:
            next_record = lang['MAINPAGE_NEXT_REC_TIME_6'].format(hours=int(hours), minutes=int(minutes))
    return next_record