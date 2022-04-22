from datetime import date
from motusAPI.models import User, Gender

# Create data for live tests
Gender.objects.create(title='männlich', icon='male.png')
Gender.objects.create(title='weiblich', icon='female.png')
Gender.objects.create(title='divers', icon='diverse.png')

male = Gender.objects.get(title='männlich')
female = Gender.objects.get(title='weiblich')

stefan = User.objects.create_user('Stefan', 'mail1@mail.de', date(1982, 3, 13), male, '123')
melissa = User.objects.create_user('Melissa', 'mail2@mail.de', date(1987, 8, 11), female, '456')
stefan.save()
melissa.save()
