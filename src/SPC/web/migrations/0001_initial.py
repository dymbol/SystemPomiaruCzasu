# Generated by Django 2.0 on 2017-12-04 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacurer', models.CharField(max_length=24)),
                ('model', models.CharField(max_length=24)),
                ('desc', models.CharField(max_length=24)),
                ('engine_model', models.CharField(blank=True, max_length=24)),
                ('fuel', models.CharField(choices=[('gasoline', 'gasoline'), ('diesel', 'diesel'), ('electricity', 'electricity')], max_length=24)),
                ('accel_type', models.CharField(blank=True, choices=[('Turbocharged', 'Turbocharged'), ('Supercharged', 'Supercharged'), ('Electrical', 'Electrical')], max_length=24)),
                ('power', models.DecimalField(blank=True, decimal_places=0, max_digits=9)),
                ('torque', models.DecimalField(blank=True, decimal_places=0, max_digits=9)),
                ('engine_capacity', models.DecimalField(decimal_places=0, max_digits=9)),
                ('wankel', models.BooleanField()),
                ('hybrid', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CarClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('type', models.CharField(choices=[('Capacity', 'Capacity'), ('AWD', 'AWD'), ('Guest', 'Guest')], max_length=24)),
                ('cap_min', models.DecimalField(decimal_places=0, max_digits=9)),
                ('cap_max', models.DecimalField(decimal_places=0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Lap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loop', models.DecimalField(decimal_places=0, max_digits=9)),
                ('taryfa', models.BooleanField()),
                ('fee', models.DecimalField(decimal_places=0, default=0, max_digits=9)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('stop_time', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('surname', models.CharField(max_length=24)),
                ('nick', models.CharField(blank=True, max_length=24)),
                ('mail', models.CharField(blank=True, max_length=24)),
                ('phone_tel', models.CharField(blank=True, max_length=24)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('race_licence', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('place', models.CharField(max_length=256)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('finished', models.BooleanField(default=False)),
                ('current_loop', models.DecimalField(decimal_places=0, default=0, max_digits=9)),
                ('race_type', models.CharField(choices=[('TimeAttack', 'TimeAttack'), ('ShorthestSum', 'ShorthestSum')], default='TimeAttack', max_length=24)),
                ('loop_count', models.DecimalField(decimal_places=0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_no', models.DecimalField(decimal_places=0, max_digits=9)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Car')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='web.Person')),
                ('navigator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='web.Person')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Race')),
            ],
        ),
        migrations.AddField(
            model_name='lap',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Race'),
        ),
        migrations.AddField(
            model_name='lap',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Team'),
        ),
    ]