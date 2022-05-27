from motusAPI.models import User, Record


def run():
    users = User.objects.all()
    for u in users:
        u.records.all().delete()





