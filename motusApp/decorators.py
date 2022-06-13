from django.shortcuts import HttpResponse

def motus_called_from_app(view_func):
    def wrapper_func(request, *args, **Kwargs):
        if request.META.get('HTTP_USER_AGENT', '') != 'motusApp':
            return HttpResponse("NUR MIT APP")
        else:
            return view_func(request, *args, **Kwargs)
    return wrapper_func 