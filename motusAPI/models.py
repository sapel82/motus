from datetime import date
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
import random
from datetime import date, datetime


class Gender(models.Model):
    """ Gender Object for user profile. """

    id = int
    objects = models.Manager()

    title = models.CharField(max_length=20)
    icon = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'gender'
        verbose_name = 'Geschlecht'
        verbose_name_plural = 'Geschlechter'
    
    def __str__(self) -> str:
        return 'Gender: {id} - {title}'.format(id=self.id, title=self.title)

    def as_dict(self) -> dict:
        return {'id': self.id, 'title': self.title, 'icon': self.icon}


class MoodFactor(models.Model):
    """ Abstract class for mood factors ressources/stressors """
    id = int
    objects = models.Manager()

    title = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return 'Ressource: {id} - {title}'.format(id=self.id, title=self.title)

    def as_dict(self) -> dict:
        return {'id': self.id, 'title': self.title, 'icon': self.icon}


class Ressource(MoodFactor):
    """ Ressource object for user profile and records """
    class Meta(MoodFactor.Meta):
        managed = True
        ordering = ['title']
        db_table = 'ressource'
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressourcen'


class Stressor(MoodFactor):
    """ Stressor object for user profile and records """
    class Meta(MoodFactor.Meta):
        managed = True
        ordering = ['title']
        db_table = 'stressor'
        verbose_name = 'Stressor'
        verbose_name_plural = 'Stressoren'


class UserManager(BaseUserManager):
    """ User Manager """
    def create_user(self, username: str, email: str, date_of_birth: date, gender: Gender, password: str):
        """
        Create a new user

        :param username: username of the user
        :param email: email of the user
        :param date_of_birth: birthdate of the user
        :param gender: gender of the user
        :param password: password of the user
        :return: user object
        """
        if not all([username, email, date_of_birth, gender, password]):
            raise ValueError('Missing userdata')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            gender=gender
        )

        user.set_password(password)
        user.activation_code = self.create_activation_code(7)

        user.save(using=self._db)
        return user

    @staticmethod
    def create_activation_code(length: int) -> int:
        min_value = pow(10, length-1)
        max_value = pow(10, length) - 1
        return random.randint(min_value, max_value)


class RecordManager(models.Manager):
    """ Record Manager """
    def user_records_today(self, user):
        now = timezone.now()
        morning = self.get_queryset().filter(user=user, timestamp__range=(now.replace(hour=0, minute=0), now.replace(hour=11, minute=59)))
        noon =self.get_queryset().filter(user=user, timestamp__range=(now.replace(hour=12, minute=0), now.replace(hour=17, minute=59)))
        evening =self.get_queryset().filter(user=user, timestamp__range=(now.replace(hour=18, minute=0), now.replace(hour=23, minute=59)))

        return (morning, noon, evening)

    def user_records_for_day(self, user, date):
        records = self.get_queryset().filter(user=user, timestamp__range=(date.replace(hour=0, minute=0), date.replace(hour=23, minute=59)))
        return records

    def user_records(self, user):
        records = self.get_queryset().filter(user=user)
        return records


class Record(models.Model):
    """ Record object """

    id = int
    objects = RecordManager()

    timestamp = models.DateTimeField(verbose_name='Zeitpunkt der Aufzeichnung')
    mood = models.IntegerField(verbose_name='Stimmung')
    note = models.CharField(max_length=255, verbose_name='Notiz')

    ressources = models.ManyToManyField(Ressource)
    stressors = models.ManyToManyField(Stressor)

    class Meta():
        managed = True
        db_table = 'record'
        verbose_name = 'Aufzeichnung'
        verbose_name_plural = 'Aufzeichnungen'

    def __str__(self) -> str:
        return 'Record: {id} - {ts} - {mood} - {note}'.format(id=self.id, ts=self.timestamp, mood=self.mood, note=self.note)

    def as_dict(self) -> dict:
        return {}


class User(AbstractBaseUser):
    """ User object """

    id = int
    objects = UserManager()

    username = models.CharField(max_length=30, unique=True, verbose_name='Benutzername')
    email = models.EmailField(max_length=255, unique=True, verbose_name='E-Mail Adresse')
    date_of_birth = models.DateField(auto_now=False, blank=True, verbose_name='Geburtsdatum')
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, verbose_name='Geschlecht')
    activation_code = models.IntegerField(unique=True, default=123456789, verbose_name='Aktivierungscode')
    language = models.CharField(max_length=5, default='de_DE', verbose_name='Gewählte Sprache')
    profile_level = models.IntegerField(default=0, verbose_name='Profilkomplettierung')
    last_visit = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Letzter Login')
    records = models.ManyToManyField(Record)
    ressources = models.ManyToManyField(Ressource)
    stressors = models.ManyToManyField(Stressor)

    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # staff
    admin = models.BooleanField(default=False)  # superuser

    USERNAME_FIELD = 'username'

    class Meta:
        managed = True
        db_table = 'user'
        verbose_name = 'Benutzer'
        verbose_name_plural = 'Benutzer'

    @property
    def is_staff(self) -> models.BooleanField:
        """ Is the user a staff member?"""
        return self.staff

    @property
    def is_admin(self) -> models.BooleanField:
        """ Is the user a admin member?"""
        return self.admin

    @property
    def is_account_active(self) -> models.BooleanField:
        """ Is the user account active? """
        return self.is_active

    def can_add_record(self) -> models.BooleanField:
        """ 
        Can the user add a new record? 

        A user can add a record up to three times a day, but only add one record
        at a specific time range. (00:00 - 12:00, 12:00 - 18:00, 18:00 - 00:00)
        """
        now = timezone.now()
        records_today = Record.objects.user_records_today(self)

        if (now.hour >= 0 and now.hour < 12 and len(records_today[0]) == 0) or \
           (now.hour >= 12 and now.hour < 18 and len(records_today[1]) == 0) or \
           (now.hour >= 18 and now.hour < 24 and len(records_today[2]) == 0):
            return True
        return False
        
    def __str__(self) -> str:
        return 'Profile: {id} - {username} - {gender} - {email}'.format(
            id=self.id, username=self.username, gender=self.gender, email=self.email
        )

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.username,
            'age': self.age,
            'gender': self.gender
        }
