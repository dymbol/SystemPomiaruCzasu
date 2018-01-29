from django.db import connections
from web.models import Race, Lap, Team, Track
from web import tinydb_con
from operator import itemgetter
from tinydb import  where


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def update(race_id):
    if Race.objects.filter(id=race_id).exists() is not True:
        return 1

    print("Updating result in memory database...")
    context = {}    #used as context in generating page from template
    cursor = connections['default'].cursor()

    context["classes_laps"]=[]

    #teams = Team.objects.filter(race__id=request.session['chosen_race_id'])
    teams = Team.objects.filter(race__id=race_id)

    #different over race type
    #  TIME ATTACK
    # - podział na klasy
    # - najniższy wynik wygrywa

    thisrace=Race.objects.filter(id=race_id)[0]
    # TODO TimeAttack Algorythm: change it like ShorthestSum
    if thisrace.race_type == "TimeAttack":
        try:
            max_result = Lap.objects.filter(track__race__id=race_id).order_by('result')[0]   # best result
        except:
            print("No laps !!!")


        # ////// classes results //////
        # get only classes wich are used in this race
        this_race_classes_query='''
            SELECT team.tclass_id, klasa.name
            FROM web_carclass klasa
            JOIN web_team team ON team.tclass_id=klasa.id
            WHERE team.race_id={}
            GROUP BY team.tclass_id
            '''.format(race_id)
        cursor.execute(this_race_classes_query)
        for klasa in cursor.fetchall():
            # fields: TARYFA_TIME, LAP_ID, TEAM_ID, START_NO, TARYFA, FEE, MIN_RESULT, RESULT_WITH_FEE, OVERALL_TIME


            # SQLITE CASE:
            # CASE WHEN (l.taryfa*1.5*{0}) IS 0 THEN (l.result+(l.fee*1000)) ELSE (l.taryfa*1.5*{1}) END AS OVERALL_TIME

            #MYSQL CASE:
            # CASE l.taryfa WHEN 1 THEN(l.taryfa * 1.5 * {0}) ELSE (l.result + (l.fee * 1000)) END AS OVERALL_TIME

            query_result_by_class='''
                SELECT  team.start_no AS START_NO, team.id as TEAM_ID, MIN(l.result+(l.fee*1000)) AS MIN_RESULT
                        from web_lap l
                        JOIN web_track track ON l.track_id=track.id
                        JOIN web_team team ON l.team_id=team.id
                        JOIN web_person person ON team.driver_id=person.id
                        WHERE track.race_id={0}
                        AND  team.tclass_id={1}
                        AND l.taryfa=0 
                        GROUP BY l.team_id
                        ORDER BY  MIN_RESULT
            '''.format(race_id, klasa[0])    # pass carclass id to query

            cursor.execute(query_result_by_class)

            # create list with carclasses names (used in template)
            context["classes_laps"].append({klasa[1]: dictfetchall(cursor)})

        # ////// general results //////

        # fields: TARYFA_TIME, LAP_ID, TEAM_ID, START_NO, TARYFA, FEE, MIN_RESULT, RESULT_WITH_FEE, OVERALL_TIME

        query = '''
            SELECT  team.start_no AS START_NO, team.id as TEAM_ID, MIN(l.result+(l.fee*1000)) AS MIN_RESULT
            from web_lap l
            JOIN web_track track ON l.track_id=track.id
            JOIN web_team team ON l.team_id=team.id
            JOIN web_person person ON team.driver_id=person.id
            WHERE track.race_id={0}
            AND l.taryfa=0
            GROUP BY l.team_id
            ORDER BY MIN_RESULT
        '''.format(race_id)
        cursor.execute(query)

        context["teams"] = teams
        context["general_laps"] = dictfetchall(cursor)
        context["race_laps"] = Track.objects.filter(race__id=race_id)
    elif thisrace.race_type == "ShorthestSum":
        #get teams on that race
        this_race_teams = Lap.objects.filter(track__race__id=race_id).order_by().values('team_id').distinct()
        this_race_laps = Lap.objects.filter(track__race__id=race_id)
        this_race_classes = Lap.objects.filter(track__race__id=race_id).order_by().values('team__tclass__name').distinct()
        gen_team_laps = []


        #general classification
        for team in this_race_teams:
            '''
                result of this loop:
                [team_id, Decimal(SUM_OF_TIMES_OF_THIS_RACE)]
            '''
            team_id = team["team_id"]
            tmp_list = []
            tmp_list.append(team_id)
            final_sum = 0
            for lap in this_race_laps:
                if team_id == lap.team.id:
                    final_sum = final_sum+lap.final_result_gen     # final_result is computed value from Lap model

            tmp_list.append(final_sum)
            gen_team_laps.append(tmp_list)

        # classes classification
        classes_team_laps = {}
        for klasa in this_race_classes:
            klasa_name = klasa['team__tclass__name']
            klasa_tmp_list = [] # for storing teams's laps per class
            for team in this_race_teams:
                '''
                    result of this loop:
                    [team_id, Decimal(SUM_OF_TIMES_OF_THIS_RACE)]
                '''
                team_id = team["team_id"]
                team_obj = Team.objects.filter(id=team_id)[0]
                if team_obj.tclass.name == klasa_name:  # PRE CHECK if team belongs to class
                    this_team_laps = []
                    final_sum = 0
                    this_team_laps.append(team_id)  # FIRST add TEAM

                    for lap in Lap.objects.filter(team=team_obj):   # SECOND compute SUM of times
                        final_sum = final_sum + lap.final_result_klasa

                    this_team_laps.append(final_sum)    # THIRD add SUM of times
                    klasa_tmp_list.append(this_team_laps)   # FOURTH ADD whole all this team laps to ceratin class

            classes_team_laps[klasa_name]=sorted(klasa_tmp_list, key=itemgetter(1)) # add sorted laps for certain klasa

        context["general_laps"] = sorted(gen_team_laps, key=itemgetter(1))       #laps for GENERAL CLASIFICATION
        context["classes_laps"] = classes_team_laps                            #laps for KLASSES  CLASIFICATION divided on classes (dict)
        context["race_tracks"] = Track.objects.filter(race__id=race_id)   #list of tracks in this race

    #ZAPIS do TinyDB
    if tinydb_con.tiny_db.contains(where('race_id') == race_id):

        print("Updating results in memory database")
        tinydb_con.tiny_db.update({'race_id': race_id, 'context': context}, where('race_id') == race_id)
    else:
        tinydb_con.tiny_db.insert({'race_id': race_id, 'context': context})



def get(race_id):
    if tinydb_con.tiny_db.contains(where('race_id') == race_id):
        ret = {"msg": "OK", "result": tinydb_con.tiny_db.search(where('race_id') == race_id)}
        return ret
    else:
        #results not generater or there is no laps
        #lets generate them:
        print("No results stored in memory database...")
        results = update(race_id)
        if results == 1:
            ret = {"msg": "No race with id {}".format(race_id), "result": 1}
            return ret
        else:
            ret = {"msg": "OK", "result": tinydb_con.tiny_db.search(where('race_id') == race_id)}
            return ret



