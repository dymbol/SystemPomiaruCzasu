# Generated by Django 2.0 on 2017-12-07 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_remove_lap_loop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='current_loop',
        ),
        migrations.RemoveField(
            model_name='race',
            name='loop_count',
        ),
    ]