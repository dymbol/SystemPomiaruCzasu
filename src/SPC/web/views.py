from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import EditRace
from django.http import JsonResponse
from django.db import connections



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


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def results(request):
    context = {}

    teams = Team.objects.filter(race__id=request.session['chosen_race_id'])

    #different over race type
    #  TIME ATTACK
    # - podział na klasy
    # - najniższy wynik wygrywa

    #class result

    #TODO

    # general result

    #fields: TARYFA_TIME, LAP_ID, TEAM_ID, START_NO, TARYFA, FEE, MIN_RESULT, RESULT_WITH_FEE, OVERALL_TIME

    query = '''
        SELECT (l.taryfa*1.5*MAX(l.result)) AS TARYFA_TIME, l.id LAP_ID, team.id as TEAM_ID, team.start_no, l.taryfa, l.fee, MIN(l.result) AS MIN_RESULT, (l.result+(l.fee*5000)) AS RESULT_WITH_FEE,
        CASE WHEN (l.taryfa*1.5*MAX(l.result)) IS 0 THEN (l.result+(l.fee*5000)) ELSE (l.taryfa*1.5*MAX(l.result)) END AS OVERALL_TIME
        from web_lap l
        JOIN web_track track ON l.track_id=track.id
        JOIN web_team team ON l.team_id=team.id
        JOIN web_person person ON team.driver_id=person.id
        WHERE track.race_id=1
        GROUP BY l.team_id
        ORDER BY  OVERALL_TIME
    '''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dictfetchall(cursor))

    context["teams"] = teams
    context["general_laps"] = dictfetchall(cursor)
    return render(request, 'results.html', context)


def register_result(request):
    context = {}
    Teams = Team.objects.filter(race__id=request.session['chosen_race_id'])
    last_laps = []

    # get every's team last lap
    for team in Teams:
        print(team)
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
    print(last_laps)
    return render(request, 'register_result.html', context)


def race(request, race_id):
    context = {}

    if request.method == 'POST':
        form = EditRace(request.POST)
        if form.is_valid():
            request.session['current_track_id'] = form.cleaned_data['track'].id
            request.session['current_track_name'] = form.cleaned_data['track'].name
            redirect('register_result')
            print("valid")
    else:
        initial = {}
        if 'current_track_name' in request.session.keys():
            initial['track'] = Track.objects.filter(id=request.session['current_track_id'])
        form = EditRace(
            race_id=race_id,
            initial=initial
        )
        print(initial)

    # request.session['current_track'] =
    return render(request, 'race.html', {'form': form, "race_id": race_id})


def time_meter(request, team_id):
    CurrentTeam = Team.objects.filter(id=team_id)[0]
    return render(request, 'time_meter.html', {'team': CurrentTeam})


def save_result(request, team_id, track_id, _result, _fee, _taryfa):
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
            result=abs(_result)
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


