from django.shortcuts import render

from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the acc_db index.")


def modes(request):
    return HttpResponse("modes are here")


