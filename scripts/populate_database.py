from datetime import date
from motusAPI.models import User, Gender, Ressource, Stressor


def run():
    # Create data for live tests
    Gender.objects.create(title='männlich', icon='male.png')
    Gender.objects.create(title='weiblich', icon='female.png')
    Gender.objects.create(title='divers', icon='non_binary.png')
    Gender.objects.create(title='keine Angabe', icon='not_available.png')

    male = Gender.objects.get(title='männlich')
    female = Gender.objects.get(title='weiblich')

    stefan = User.objects.create_user('Stefan', 'sta1701d@googlemail.com', date(1982, 3, 13), male, 'endor')
    melissa = User.objects.create_user('Mel', 'mellimel1108@googlemail.com', date(1987, 8, 11), female, 'utopia.150515mo')

    Ressource.objects.create(title='Tiere', icon='animals.png')
    Ressource.objects.create(title='Kunst', icon='art.png')
    Ressource.objects.create(title='Backen', icon='baking.png')
    Ressource.objects.create(title='Baden', icon='bath.png')
    Ressource.objects.create(title='Brettspiele', icon='boardgames.png')
    Ressource.objects.create(title='Aufräumen', icon='cleaning.png')
    Ressource.objects.create(title='Kochen', icon='cooking.png')
    Ressource.objects.create(title='Familie', icon='family.png')
    Ressource.objects.create(title='Freunde', icon='friends.png')
    Ressource.objects.create(title='Lernen', icon='learning.png')
    Ressource.objects.create(title='Filme', icon='movies.png')
    Ressource.objects.create(title='Musik', icon='music.png')
    Ressource.objects.create(title='Natur', icon='nature.png')
    Ressource.objects.create(title='Lesen', icon='reading.png')
    Ressource.objects.create(title='Entspannung', icon='relax.png')
    Ressource.objects.create(title='Shopping', icon='shopping.png')
    Ressource.objects.create(title='Schlafen', icon='sleeping.png')
    Ressource.objects.create(title='Sport', icon='sport.png')
    Ressource.objects.create(title='Videospiele', icon='videogames.png')
    Ressource.objects.create(title='Partnerschaft', icon='love.png')

    Stressor.objects.create(title='Grübeln', icon='ponder.png')
    Stressor.objects.create(title='Stress', icon='stress.png')
    Stressor.objects.create(title='Arbeit', icon='work.png')
    Stressor.objects.create(title='Nachrichten', icon='news.png')    
    Stressor.objects.create(title='Politik', icon='politics.png')    
    Stressor.objects.create(title='Konzentration', icon='concentration.png')    
    Stressor.objects.create(title='Sorgen', icon='worries.png')
    Stressor.objects.create(title='Liebeskummer', icon='heartache.png')
    Stressor.objects.create(title='Schmerzen', icon='pain.png')
    Stressor.objects.create(title='Schlafmangel', icon='insomnia.png')
    Stressor.objects.create(title='Erschöpfung', icon='exhaustion.png')
    Stressor.objects.create(title='Alptraum', icon='nightmare.png')
    Stressor.objects.create(title='Angst', icon='anxiety.png')






