from django import template
from django.template.defaultfilters import stringfilter
from web.models import Team, Lap, Track, Race
register = template.Library()
import datetime
from decimal import Decimal
from django.conf import settings

@register.filter
def GetTeamName(value):
    """get Team Name by the given id"""
    if type(value) is int:
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
def GetTeamStartNo(value):
    if type(value) is int:
        team = Team.objects.filter(id=value)
        return team[0].start_no




@register.filter
def msToHumanTime(value):
    """Changes millisecond to format M:S:m"""
    if type(value) is int or type(value) is Decimal:

        if type(value) is Decimal:
            value = int(value)

        my_time = datetime.datetime.fromtimestamp(value / 1000.0)
        return "{}:{}:{}".format(my_time.minute, my_time.second, int(my_time.microsecond / 1000))
    else:
        return '-'


@register.filter
def GetTeamLaps(value):
    """get Team laps by the given team_id"""
    if type(value) is int:
        results=[]
        team = Team.objects.filter(id=value)
        laps = Lap.objects.filter(team=value)
        tracks = Track.objects.filter(race=team[0].race)


        for track in tracks:
            lap = Lap.objects.filter(track__id=track.id, team=value)
            if lap.exists():
                Kary = ""
                if lap[0].taryfa is True:   # if taryfa show letter T
                    Kary = Kary + " (T)"
                if lap[0].fee > 0:
                    Kary = Kary+"(+"+str(lap[0].fee)+"s)"

                if lap[0].taryfa is True:   #if "taryfa" show the taryfa time. If not show real time
                    result = lap[0].result_taryfa_klasa
                else:
                    result = lap[0].result
            else:
                result = '<i class="fa fa-minus-square" aria-hidden="true"></i>'
                Kary = ""

            results.append("{} {}".format(msToHumanTime(result), Kary))

        #if no lap at track insert "-" value
        for track_no in range(len(tracks)):
            try:
                type(results[track_no])
            except:
                results.append('-')


        return results


@register.simple_tag
def GetGoogleAnalitycsConfig():
    return settings.GACONFIG
