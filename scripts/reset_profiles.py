from motusAPI.models import User


def run():
    stefan = User.objects.filter(username='Stefan').first()
    stefan.profile_level = 0
    stefan.save()

    # users = User.objects.all()
    # for u in users:
    #     u.profile_level = 0
    #     u.save()






