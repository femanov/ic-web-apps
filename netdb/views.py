from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Domain, Net

def index(request):
    doms = Domain.objects.all()
    nets = Net.objects.all()
    output = ', '.join([d.name for d in doms])
    return HttpResponse(output)




