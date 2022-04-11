from motusAPI.models import Profile, Gender


# Create data for live tests
Gender.objects.create(title='männlich', icon='male.png')
Gender.objects.create(title='weiblich', icon='female.png')
Gender.objects.create(title='divers', icon='diverse.png')

Profile.objects.create(
    username='Stefan',
    email='sta1701d@googlemail.com',
    age=40,
    gender=Gender.objects.get(title='männlich')
)
Profile.objects.create(
    username='Melissa',
    email='mellimel1108@googlemail.com',
    age=34,
    gender=Gender.objects.get(title='weiblich')
)

male = Gender.objects.get(title='männlich')
female = Gender.objects.get(title='weiblich')
divers = Gender.objects.get(title='divers')

stefan = Profile.objects.get(username='Stefan')
melissa = Profile.objects.get(username='Melissa')

male.save()
female.save()
divers.save()

stefan.save()
melissa.save()
