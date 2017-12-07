from django import template
from django.template.defaultfilters import stringfilter
from web.models import Team
from web.models import Lap
register = template.Library()
import datetime

@register.filter
def GetTeamName(value):
    """get Team Name by the given id"""
    team = Team.objects.filter(id=value)
    print(team)
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
    laps = Lap.objects.filter(team=value)

    for lap in laps:
        Kary = ""
        if lap.taryfa is True:
            Kary = Kary + "(T)"
        if lap.fee > 0:
            Kary = Kary+"(+"+str(lap.fee)+"s)"

        results.append("{} {}".format(msToHumanTime(lap.result),Kary))

    return results
