from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=24)
    surname = models.CharField(max_length=24)
    nick = models.CharField(max_length=24, blank=True)
    mail = models.CharField(max_length=24, blank=True)
    phone_tel = models.CharField(max_length=24, blank=True)
    desc = models.CharField(max_length=200, blank=True)
    race_licence = models.BooleanField()

    def __str__(self):
        return "{} {} ({})".format(self.name, self.surname, self.nick)


class Race(models.Model):
    name = models.CharField(max_length=256)
    place = models.CharField(max_length=256)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    finished = models.BooleanField(default=False)   # True id Race is finished
    current_loop = models.DecimalField(default=0, decimal_places=0, max_digits=9)
    race_type_choices = (
        ('TimeAttack', 'TimeAttack'),
        ('ShorthestSum', 'ShorthestSum')
        )

    race_type = models.CharField(
        choices=race_type_choices,
        default='TimeAttack',
        max_length=24
    )
    loop_count = models.DecimalField(decimal_places=0, max_digits=9)     # how many loops are on race

    def __str__(self):
        return self.name


class CarClass(models.Model):
    name = models.CharField(max_length=24)
    type_choices = (
        ('Capacity','Capacity'),
        ('AWD', 'AWD'),
        ('Guest', 'Guest')
    )
    type = models.CharField(
        choices=type_choices,
        max_length=24
    )
    cap_min = models.DecimalField(decimal_places=0, max_digits=9)       # used if type='Capacity', unit: ccm
    cap_max = models.DecimalField(decimal_places=0, max_digits=9)       # used if type='Capacity', unit: ccm

    def __str__(self):
        return self.name


class Car(models.Model):
    manufacurer = models.CharField(max_length=24, )
    model = models.CharField(max_length=24, )
    desc = models.CharField(max_length=24, )
    engine_model = models.CharField(max_length=24, blank=True)
    fuel_choices = (
        ("gasoline", "gasoline"),
        ("diesel", "diesel"),
        ("electricity", "electricity")
    )
    fuel = models.CharField(choices=fuel_choices, max_length=24)
    accel_type_choices = (
        ("Turbocharged","Turbocharged"),
        ("Supercharged","Supercharged"),
        ("Electrical","Electrical")
    )
    accel_type = models.CharField(
        choices=accel_type_choices,
        blank=True,
        max_length=24
    )

    power = models.DecimalField(decimal_places=0, max_digits=9, blank=True)     # unit: Horse Power (KM)
    torque = models.DecimalField(decimal_places=0, max_digits=9, blank=True)     # unit: Nm
    engine_capacity = models.DecimalField(decimal_places=0, max_digits=9)   #unit: ccm
    wankel = models.BooleanField()
    hybrid = models.BooleanField()

    def __str__(self):
        return "{} {} {}".format(self.manufacurer, self.model, round(self.engine_capacity/1000, 1))


class Team(models.Model):
    start_no = models.DecimalField(decimal_places=0, max_digits=9)
    driver = models.ForeignKey(Person, on_delete=models.CASCADE,related_name='+',)
    navigator = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, related_name='+',)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        team_name = "{}.{}, {}.{}".format(
            self.driver.name[:1],
            self.driver.surname,
            self.navigator.name[:1],
            self.navigator.surname
            )
        print(team_name)
        return "{}: {}".format(self.start_no, team_name)


class Lap(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    loop = models.DecimalField(decimal_places=0, max_digits=9)
    taryfa = models.BooleanField()  # true if "taryfa"
    fee = models.DecimalField(default=0, decimal_places=0, max_digits=9)   # fee in seconds
    start_time = models.TimeField(blank=True, null=True)
    stop_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "{}, {}, Loop: {}".format(self.race, self.team, self.loop)
