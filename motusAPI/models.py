from datetime import date
from operator import length_hint, truediv
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
import random


class Gender(models.Model):
    """ Gender Object for user profile. """

    id = int
    objects = None

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
    objects = None

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


class RecordManager(models.Manager):
    """ Record Manager """
    def records_today(self):
        pass


class Record(models.Model):
    """ Record object """

    id = int
    objects = None

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
        return ''

    def as_dict(self) -> dict:
        return {}