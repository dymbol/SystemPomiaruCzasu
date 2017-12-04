from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.models import *

# Create your views here.


def index(request):
    context = {}
    context["races"] = Race.objects.all() #.dates('creation_date', 'year').distinct()

    return render(request, 'index.html', context)
