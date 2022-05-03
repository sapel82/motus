from motusAPI.models import User, Ressource


def run():
    stefan = User.objects.get(username='Stefan')
    mel = User.objects.get(username='Mel')

    stefan.ressources.clear()
    mel.ressources.clear()

    backen = Ressource.objects.get(title='Backen')
    tiere = Ressource.objects.get(title='Tiere')
    baden = Ressource.objects.get(title='Baden')
    schlafen = Ressource.objects.get(title='Schlafen')

    videospiele = Ressource.objects.get(title='Videospiele')
    filme = Ressource.objects.get(title='Filme')
    musik = Ressource.objects.get(title='Musik')
    natur = Ressource.objects.get(title='Natur')

    mel.ressources.add(backen, tiere, baden, schlafen)
    stefan.ressources.add(videospiele, filme, musik, natur)

    print(stefan, stefan.ressources.all())
    print(mel, mel.ressources.all())




