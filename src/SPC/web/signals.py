'''
based on
https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html

important: code also in ready function in web/apps.py
'''
from web import result_functions
from web.models import Lap
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Lap)
def update_results_in_memdb(sender, instance, **kwargs):
    result_functions.update(instance.track.race_id)