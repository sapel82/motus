from datetime import datetime
from motusAPI.models import User, Gender

# Create data for live tests
Gender.objects.create(title='männlich', icon='male.png')
Gender.objects.create(title='weiblich', icon='female.png')
Gender.objects.create(title='divers', icon='diverse.png')

male = Gender.objects.get(title='männlich')
female = Gender.objects.get(title='weiblich')

stefan = User.objects.create_user('Stefan', 'mail1@mail.de', datetime(1982, 3, 13, 0, 0, 0), male, '123')
melissa = User.objects.create_user('Melissa' 'mai2l@mail.de', datetime(1987, 8, 11, 0, 0, 0), female, '456')
