from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import EditRace
from django.http import JsonResponse
from django.db import connections
from django.db.models.query import QuerySet
from web import result_functions



# TODO admin panel: filter teams by race, filter tracks by race etc

def index(request):
    context = {}
    context["races"] = Race.objects.all()  # .dates('creation_date', 'year').distinct()
    if "chosen_race_id" in context.keys():
        context["chosen_race_id"] = request.session['chosen_race_id']       # get the id of chosen race
    return render(request, 'index.html', context)



def race_list(request):
    context = {}
    context["races"] = Race.objects.all()  # .dates('creation_date', 'year').distinct()
    if "chosen_race_id" in context.keys():
        context["chosen_race_id"] = request.session['chosen_race_id']       # get the id of chosen race
    return render(request, 'race_list.html', context)


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
    return redirect('results')
    # TODO return page with race information


def team_list(request):
    if "chosen_race_id" not in request.session.keys():
        return redirect('race_list')
        # TODO add messaege: Wybierz wyścig z listy poniżej
    context = {}
    context["teams"] = Team.objects.filter(race__id=request.session['chosen_race_id']).order_by('start_no')
    # TODO add page with info about every team

    return render(request, 'teams.html', context)


def results(request):
    '''get result data from memory database'''
    if "chosen_race_id" not in request.session.keys():
        return redirect('race_list')
        # TODO add messaege: Wybierz wyścig z listy poniżej
    context = {}
    thisrace = Race.objects.filter(id=request.session['chosen_race_id'])[0]
    if thisrace.race_type == "TimeAttack":
        res = result_functions.get(request.session['chosen_race_id'])
        if res["result"] is not 1:
            return render(request, 'results_time_attack.html', res['result'][0]['context'])
        else:
            return redirect('index')
    elif thisrace.race_type == "ShorthestSum":
        res = result_functions.get(request.session['chosen_race_id'])
        #print(res)
        if res["result"] is not 1:
            return render(request, 'results_sum.html', res['result'][0]['context'])
        else:
            return redirect('index')


@login_required
def register_result(request):
    if "chosen_race_id" not in request.session.keys():
        return redirect('index')
    if "current_track_id" not in request.session.keys():
        return redirect('race',request.session['chosen_race_id'])
    context = {}
    Teams = Team.objects.filter(race__id=request.session['chosen_race_id'])
    last_laps = []

    # get every's team last lap
    for team in Teams:
        # get last recordered lap
        if Lap.objects.filter(track__race__id=request.session['chosen_race_id'], team__id=team.id).exists():
            lap_tmp = Lap.objects.filter(track__race__id=request.session['chosen_race_id'], team__id=team.id).order_by('-stop_time')[0]
            lap_tmp_track = lap_tmp.track
        else:
            lap_tmp_track = "brak"
        last_laps.append({
            "id": str(team.id),
            "start_no": str(team.start_no),
            "driver": team.driver,
            "navigator": team.navigator,
            "last_lap": "Trasa: {}".format(lap_tmp_track)
        })
    context["last_laps"] = last_laps
    result_functions.update(request.session['chosen_race_id'])
    return render(request, 'register_result.html', context)


@login_required
def change_track(request, race_id):
    context = {}

    if request.method == 'POST':
        form = EditRace(request.POST)
        if form.is_valid():
            request.session['current_track_id'] = form.cleaned_data['track'].id
            request.session['current_track_name'] = form.cleaned_data['track'].name
            redirect('register_result')
    else:
        initial = {}
        if 'current_track_name' in request.session.keys():
            initial['track'] = Track.objects.filter(name=request.session['current_track_name'])[0].id

        form = EditRace(
            race_id=race_id,
            initial=initial
        )

    # request.session['current_track'] =
    return render(request, 'change_track.html', {'form': form, "race_id": race_id})

@login_required
def time_meter(request, team_id):
    CurrentTeam = Team.objects.filter(id=team_id)[0]
    return render(request, 'time_meter.html', {'team': CurrentTeam})


@login_required
def save_result(request, team_id, track_id, _result, _fee, _taryfa):
    '''result are saved in memory database'''
    error_msgs = []
    # checks
    if not Team.objects.filter(id=team_id).exists():
        error_msgs.append("Team with id: {} doesn't exist".format(team_id))
    if not Track.objects.filter(id=track_id).exists():
        error_msgs.append("Track with id: {} doesn't exist".format(track_id))
    if not type(_result) == int:
        error_msgs.append("Result: digit required")
    if not type(_fee) == int:
        error_msgs.append("Fee: digit required")
    if Lap.objects.filter(team__id=team_id, track__id=track_id,).exists():
        error_msgs.append("Lap with that track already registered!")

    if len(error_msgs) > 0:
        data = {
            "status": "nok",
            "msg": error_msgs
        }

    else:
        new_lap = Lap(
            team=Team.objects.filter(id=team_id)[0],
            track=Track.objects.filter(id=track_id)[0],
            fee=abs(_fee),
            result=abs(_result),
        )
        if _taryfa == 1:
            new_lap.taryfa = True
        else:
            new_lap.taryfa = False

        new_lap.save()

        data = {
            "status": "ok"
        }

    return JsonResponse(data)


