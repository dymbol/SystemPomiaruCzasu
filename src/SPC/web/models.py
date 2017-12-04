from django.db import models

# Create your models here.


class Racer(models.Model):
    name = models.CharField(max_length=24, required=True)
    surname = models.CharField(max_length=24, required=True)
    nick = models.CharField(max_length=24)
    mail = models.CharField(max_length=24)
    phone_tel = models.CharField(max_length=24)
    desc = models.CharField(max_length=200)
    race_licence = models.BooleanField(required=True)




class Race(models.Model):
    name = models.CharField(max_length=24, required=True)
    place = models.CharField(max_length=24, required=True)
    date = models.DateTimeField()

    # for example: 1 - time attack, 2 - KJS style
    race_type = models.DecimalField(decimal_places=0, max_digits=9, required=True)
    loop_count = models.DecimalField(decimal_places=0, max_digits=9, required=True)     # how many loops are on race


class CarClass(models.Model):
    name = models.CharField(max_length=24, required=True)
    cap_measurement = models.BooleanField(required=True)    # true if this class is engine's capacity based
    awd_measurement = models.BooleanField(required=True)  # true if this class is awd(all wheel drive) based
    guest = models.BooleanField(required=True)  # true if this class is only for race licence racers
    cap_min = models.DecimalField(decimal_places=0, max_digits=9)       # used if cap_measurment=True, unit: ccm
    cap_max = models.DecimalField(decimal_places=0, max_digits=9)       # used if cap_measurment=True, unit: ccm


class Car(models.Model):
    manufacurer = models.CharField(max_length=24, required=True)
    model = models.CharField(max_length=24, required=True)
    desc = models.CharField(max_length=24, required=True)

    # 1 - gasoline, 2 - diesel, 3 -  electrical, 4 - hybrid
    fuel = models.DecimalField(decimal_places=0, max_digits=2)

    # 1 - turbo, 2 - compressor, 3 - electrical, 4 - airpump
    accel_type = models.DecimalField(decimal_places=0, max_digits=2)

    power = models.DecimalField(decimal_places=0, max_digits=9)     # unit: Horse Power (KM)
    torque = models.DecimalField(decimal_places=0, max_digits=9)     # unit: Nm
    engine_capacity = models.DecimalField(decimal_places=0, max_digits=9)   #unit: ccm
    wankel = models.BooleanField(required=True)
    turbocharged = models.BooleanField(required=True)
    supercharged = models.BooleanField(required=True)
    hybrid = models.BooleanField(required=True)


class Participant(models.Model):
    race = models.ForeignKey(Race)
    racer = models.ForeignKey(Racer)
    car = models.ForeignKey(Car)



class Loop(models.Model):
    no = models.DecimalField(decimal_places=0, max_digits=9)     # id of loop
    finished = models.BooleanField(required=True)       # true if that loop was finsihed


class Lap(models.Model):
    race = models.ForeignKey(Race)
    participant = models.ForeignKey(Participant)
    loop = models.ForeignKey(Loop)
    taryfa = models.BooleanField(required=True) # true if "taryfa"
    fee = models.DecimalField(decimal_places=0, max_digits=9)   # fee in seconds
    start_time = models.TimeField()
    stop_time = models.TimeField()