from django.db.models import Model, IntegerField, CharField, ForeignKey, DO_NOTHING


class Gender(Model):
    """
    Gender Object for user profile.

    Args:
        title (str): name of the gender
        icon (str): icon file used for the gender
    Returns:
        Gender (class)
    """

    id = int
    objects = None

    title = CharField(max_length=20)
    icon = CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'gender'
        verbose_name = 'Geschlecht'
        verbose_name_plural = 'Geschlechter'
    
    def __str__(self) -> str:
        return 'Gender: {id} - {title}'.format(id=self.id, title=self.title)

    def as_dict(self) -> dict:
        return {'id': self.id, 'title': self.title, 'icon': self.icon}


class Profile(Model):
    """ Profile object.
    
    Args:
        username (str): username/nickname of the user
        email (str): email adress of the user
        age (int): age of the user
        gender (Gender): gender of the user
    Returns:
        Profile (class)
    """
    # TODO: one to one link with django auth_user

    id = int
    objects = None

    username = CharField(max_length=30)
    email = CharField(max_length=50)
    age = IntegerField()
    gender = ForeignKey(Gender, on_delete=DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'profile'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'

    def __str__(self) -> str:
        return 'Profile: {id} - {username} - {age} - {gender} - {email}'.format(
            id=self.id, username=self.username, age=self.age, gender=self.gender, email=self.email
        )

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.username,
            'age': self.age,
            'gender': self.gender
        }
