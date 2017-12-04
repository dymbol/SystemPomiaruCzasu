from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.models import *

# Create your views here.
@login_required(login_url='login_user')
def index(request):
    context = {}
    races = []

    if request.user.groups.values_list('name', flat=True).count() == 0:
        #user doesn't belong to any group
        print("User {} doesn't belong to any group".format(request.user.username))
    else:
        #get albums list for that user
        races = Race.objects.all().dates('creation_date', 'year').distinct()
        context["races"] = races

    return render(request, 'index.html', context)
