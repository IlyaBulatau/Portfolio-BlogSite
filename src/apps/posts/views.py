from django.http import HttpResponse


def healthchek(request):
    return HttpResponse({"Data": "Ok"})