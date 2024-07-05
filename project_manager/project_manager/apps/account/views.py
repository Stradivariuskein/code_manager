from django.shortcuts import render
from django.http import HttpResponse

def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)
