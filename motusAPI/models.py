from datetime import date
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
