from django.utils import timezone
from dateutil.parser import parse
from motusAPI.models import User

class LastVisitMiddleware(object):
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):

        LAST_VISIT_INTERVAL = 300
        now = timezone.now()

        if request.user.is_authenticated:
            last_visit = request.session.get('last_visit')
            if not last_visit or (now - parse(last_visit)).seconds > LAST_VISIT_INTERVAL:
                User.objects.filter(username=request.user.username).update(last_visit=now)
                request.session['last_visit'] = now.isoformat()

        response = self.get_response(request)

        return response