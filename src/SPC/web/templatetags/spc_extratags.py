from django import template
from django.template.defaultfilters import stringfilter
from web.models import Team, Lap, Track, Race
register = template.Library()
import datetime

@register.filter
def GetTeamName(value):
    """get Team Name by the given id"""
    team = Team.objects.filter(id=value)
    if team[0].navigator is None:
        team_name="{}.{}".format(team[0].driver.name,team[0].driver.surname)
    else:
        team_name = "{}.{}/{}.{}".format(
            team[0].driver.name[0],
            team[0].driver.surname,
            team[0].navigator.name[0],
            team[0].navigator.surname)
    return team_name

@register.filter
def msToHumanTime(value):
    """Chnages millisecond to format M:S:m"""
    my_time = datetime.datetime.fromtimestamp(value / 1000.0)
    return "{}:{}:{}".format(my_time.minute, my_time.second, int(my_time.microsecond/1000))

@register.filter
def GetTeamLaps(value):
    """get Team laps by the given team_id"""
    results=[]
    team = Team.objects.filter(id=value)
    laps = Lap.objects.filter(team=value)
    tracks = Track.objects.filter(race=team[0].race)


    for lap in laps:
        Kary = ""
        if lap.taryfa is True:
            Kary = Kary + "(T)"
        if lap.fee > 0:
            Kary = Kary+"(+"+str(lap.fee)+"s)"

        results.append("{} {}".format(msToHumanTime(lap.result),Kary))

    #if no lap at track insert "-" value
    for track_no in range(len(tracks)):
        try:
            print(results[track_no])
        except:
            results.append("-")

    return results
