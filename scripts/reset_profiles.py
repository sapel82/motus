from motusAPI.models import User


def run():
    users = User.objects.all()
    for u in users:
        u.profile_level = 0
        u.save()






