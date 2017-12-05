from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import EditRace



def index(request):
    context = {}
    context["races"] = Race.objects.all()  # .dates('creation_date', 'year').distinct()
    context["chosen_race_id"] = request.session['chosen_race_id']       # get the id of chosen race
    return render(request, 'index.html', context)


def choose_race(request, race_id=None):
    '''

    :param request:
    :param race_id:
    :return: save id id of chosen race in that session
    '''
    if Race.objects.filter(id=race_id).exists() is True:
        request.session['chosen_race_id'] = race_id
        request.session['chosen_race_name'] = Race.objects.filter(id=race_id)[0].name
    else:
        print("Lack of race with id: {}").format(race_id)
    return redirect('index')


def team_list(request):
    context = {}
    context["teams"] = Team.objects.filter(race__id=request.session['chosen_race_id'])
    return render(request, 'teams.html', context)


def results(request):
    context = {}
    context["teams"] = Team.objects.filter(race__id=request.session['chosen_race_id'])
    return render(request, 'results.html', context)


def register_result(request):
    context = {}
    results = {}
    Teams = Team.objects.filter(race__id=request.session['chosen_race_id'])
    Tracks = Track.objects.filter(race__id=request.session['chosen_race_id'])
    last_laps = []

    #get every's team lat lap
    for team in Teams:
        # get last recordered lap
        lap_tmp = Lap.objects.filter(track__race__id=request.session['chosen_race_id']).order_by('-stop_time')[0]
        print( Lap.objects.filter(track__race__id=request.session['chosen_race_id']).reverse())
        last_laps.append({
            "start_no": str(team.start_no),
            "driver": team.driver,
            "navigator": team.navigator,
            "last_lap": "Trasa: {}, Pętla: {}".format(lap_tmp.track, lap_tmp.loop)
        })


    #for team in Teams:
    #    results[team] = {}
    #    for track in Track.objects.filter(race__id=request.session['chosen_race_id']):
    #        results[team][track] = []
    #        for lap in Lap.objects.filter(track=track, team=team):
    #            results[team][track].append(lap)
    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(results)
    context["last_laps"] = last_laps

    return render(request, 'register_result.html', context)




def race(request, race_id):
    context = {}

    if request.method == 'POST':
        form = EditRace(request.POST)
        if form.is_valid():
            request.session['current_loop'] = int(form.cleaned_data['loop'])
            request.session['current_track_id'] = form.cleaned_data['track'].id
            request.session['current_track_name'] = form.cleaned_data['track'].name
            redirect('register_result')
            print("valid")
    else:
        initial = {}
        print(request.session.keys())
        if 'current_loop' in request.session.keys():
            initial['loop'] = request.session['current_loop']
        if 'current_track_name' in request.session.keys():
            initial['track'] = Track.objects.filter(id=request.session['current_track_id'])
        form = EditRace(
            race_id=race_id,
            initial=initial
        )
        print(initial)

    #request.session['current_loop'] =
    # request.session['current_track'] =


    return render(request, 'race.html', {'form': form, "race_id": race_id})


