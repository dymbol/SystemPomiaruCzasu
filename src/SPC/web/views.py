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
    if "chosen_race_id" in context.keys():
        context["chosen_race_id"] = request.session['chosen_race_id']       # get the id of chosen race
    return render(request, 'index.html', context)

@login_required
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
    if "chosen_race_id" not in request.session.keys():
        return redirect('index')
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
    max_result=0
    if "chosen_race_id" not in request.session.keys():
        return redirect('index')

    cursor = connections['default'].cursor()
    context = {}
    context["classes_laps"]=[]

    teams = Team.objects.filter(race__id=request.session['chosen_race_id'])

    #different over race type
    #  TIME ATTACK
    # - podział na klasy
    # - najniższy wynik wygrywa

    try:
        max_result = Lap.objects.filter(track__race__id=request.session['chosen_race_id']).order_by('-result')[0]   # worst result
    except:
        print("Not any lap registered")

    # ////// classes results //////
    # get only classes wich are used in this race
    this_race_classes_query='''
        SELECT team.tclass_id, klasa.name
        FROM web_carclass klasa
        JOIN web_team team ON team.tclass_id=klasa.id
        WHERE team.race_id={}
        GROUP BY team.tclass_id
        '''.format(request.session['chosen_race_id'])
    cursor.execute(this_race_classes_query)
    for klasa in cursor.fetchall():
        # fields: TARYFA_TIME, LAP_ID, TEAM_ID, START_NO, TARYFA, FEE, MIN_RESULT, RESULT_WITH_FEE, OVERALL_TIME


        query_result_by_class='''
            SELECT (l.taryfa*1.5*{0}) AS TARYFA_TIME, l.id LAP_ID, team.id as TEAM_ID, team.start_no, l.taryfa, l.fee, MIN(l.result) AS MIN_RESULT, (l.result+(l.fee*1000)) AS RESULT_WITH_FEE,
            CASE WHEN (l.taryfa*1.5*{1}) IS 0 THEN (l.result+(l.fee*1000)) ELSE (l.taryfa*1.5*{2}) END AS OVERALL_TIME
            from web_lap l 
            JOIN web_track track ON l.track_id=track.id 
            JOIN web_team team ON l.team_id=team.id 
            JOIN web_person person ON team.driver_id=person.id 
            WHERE track.race_id=1 
            AND  team.tclass_id={3}
            AND l.taryfa=0 
            GROUP BY l.team_id
            ORDER BY  OVERALL_TIME
        '''.format(max_result.result, max_result.result,max_result.result,klasa[0])    # pass carclass id to query
        cursor.execute(query_result_by_class)

        # create list with carclasses names (used in template)
        context["classes_laps"].append({klasa[1]: dictfetchall(cursor)})

    # ////// general results //////

    # fields: TARYFA_TIME, LAP_ID, TEAM_ID, START_NO, TARYFA, FEE, MIN_RESULT, RESULT_WITH_FEE, OVERALL_TIME

    query = '''
        SELECT (l.taryfa*1.5*{0}) AS TARYFA_TIME, l.id LAP_ID, team.id as TEAM_ID, team.start_no, l.taryfa, l.fee, MIN(l.result) AS MIN_RESULT, (l.result+(l.fee*1000)) AS RESULT_WITH_FEE,
        CASE WHEN (l.taryfa*1.5*{1}) IS 0 THEN (l.result+(l.fee*1000)) ELSE (l.taryfa*1.5*{2}) END AS OVERALL_TIME
        from web_lap l
        JOIN web_track track ON l.track_id=track.id
        JOIN web_team team ON l.team_id=team.id
        JOIN web_person person ON team.driver_id=person.id
        WHERE track.race_id=1
        AND l.taryfa=0
        GROUP BY l.team_id
        ORDER BY  OVERALL_TIME
    '''.format(max_result.result,max_result.result,max_result.result)
    cursor.execute(query)
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dictfetchall(cursor))

    context["teams"] = teams
    context["general_laps"] = dictfetchall(cursor)
    context["race_laps"] = Track.objects.filter(race__id=request.session['chosen_race_id'])
    return render(request, 'results.html', context)


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
    return render(request, 'register_result.html', context)


@login_required
def race(request, race_id):
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
            initial['track'] = Track.objects.filter(id=request.session['current_track_id'])
        form = EditRace(
            race_id=race_id,
            initial=initial
        )

    # request.session['current_track'] =
    return render(request, 'race.html', {'form': form, "race_id": race_id})

@login_required
def time_meter(request, team_id):
    CurrentTeam = Team.objects.filter(id=team_id)[0]
    return render(request, 'time_meter.html', {'team': CurrentTeam})


@login_required
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
            result=abs(_result),
            result_plus_fee=abs(_result)+(abs(_fee)*1000),
            result_taryfa = 0
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


