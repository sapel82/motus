from django.test import TestCase
from motusAPI.models import Profile, Gender


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

        print('\nErstellte Objekte zu Beginn des Tests\n' + 80*'-')
        genders = Gender.objects.all()
        for g in genders:
            print(g)

        profiles = Profile.objects.all()
        for p in profiles:
            print(p)
        print(80*'-' + '\n')

    def test_profile_have_correct_gender(self):
        """Profile have correct gender?"""
        male = Gender.objects.get(title='männlich')
        female = Gender.objects.get(title='weiblich')
        stefan = Profile.objects.get(username='Stefan')
        melissa = Profile.objects.get(username='Melissa')

        self.assertEqual(stefan.gender, male)
        self.assertEqual(melissa.gender, female)

    def test_save_profile(self):
        """Profile can be saved?"""
        male = Gender.objects.get(title='männlich')
        female = Gender.objects.get(title='weiblich')

        yuna_data = {
            'username': 'Yuna',
            'email': 'pfoti@fortasshole.com',
            'age': 14,
            'gender': male
        }

        yoko_data = {
            'username': 'Yoko',
            'email': 'baumfällt@fortasshole.com',
            'age': 4,
            'gender': female
        }

        new_yuna = Profile(**yuna_data)
        new_yuna.save()

        new_yoko = Profile(**yoko_data)
        new_yoko.save()

        yuna = Profile.objects.get(id=new_yuna.id)
        yoko = Profile.objects.get(id=new_yoko.id)

        self.assertEqual(yuna.username, 'Yuna')
        self.assertEqual(yoko.username, 'Yoko')

        print('Erstellte Objekte zum Ende des Tests\n' + 80*'-')
        genders = Gender.objects.all()
        for g in genders:
            print(g)

        profiles = Profile.objects.all()
        for p in profiles:
            print(p)
        print(80*'-' + '\n')
