from django import template
from django.template.defaultfilters import stringfilter
from web.models import Team, Lap, Track, Race
register = template.Library()
import datetime

@register.filter
def GetTeamName(value):
    """get Team Name by the given id"""
    team = Team.objects.filter(id=value)
    if team[0].driver.nick is None:
        driver_nick = ""
    else:
        driver_nick = "({})".format(team[0].driver.nick)


    if team[0].navigator is None:
        team_name="{}.{} {}".format(team[0].driver.name[0], team[0].driver.surname, driver_nick)
    else:
        if team[0].navigator.nick is None:
            nav_nick = ""
        else:
            nav_nick = "({})".format(team[0].navigator.nick)

        team_name = "{}.{} {}/{}.{} {}".format(
            team[0].driver.name[0],
            team[0].driver.surname,
            driver_nick,
            team[0].navigator.name[0],
            team[0].navigator.surname,
            nav_nick)
    return team_name

@register.filter
def msToHumanTime(value):
    """Chnages millisecond to format M:S:m"""
    if type(value) is int:
        my_time = datetime.datetime.fromtimestamp(value / 1000.0)
        return "{}:{}:{}".format(my_time.minute, my_time.second, int(my_time.microsecond/1000))
    else:
        return "-"


@register.filter
def GetTeamLaps(value):
    """get Team laps by the given team_id"""
    results=[]
    team = Team.objects.filter(id=value)
    laps = Lap.objects.filter(team=value)
    tracks = Track.objects.filter(race=team[0].race)


    for track in tracks:
        print(track.id)
        lap = Lap.objects.filter(track__id=track.id, team=value)
        if lap.exists():
            Kary = ""
            if lap[0].taryfa is True:
                Kary = Kary + "(T)"
            if lap[0].fee > 0:
                Kary = Kary+"(+"+str(lap[0].fee)+"s)"
            result = lap[0].result
        else:
            result = "-"
            Kary = ""

        results.append("{} {}".format(msToHumanTime(result), Kary))

    #if no lap at track insert "-" value
    for track_no in range(len(tracks)):
        try:
            print(results[track_no])
        except:
            results.append("-")

    return results
