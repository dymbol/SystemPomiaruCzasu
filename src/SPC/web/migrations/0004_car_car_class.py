# Generated by Django 2.0 on 2017-12-05 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20171204_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='web.CarClass'),
            preserve_default=False,
        ),
    ]