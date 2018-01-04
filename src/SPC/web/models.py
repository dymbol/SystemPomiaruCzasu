from django.db import models
class Person(models.Model):
    name = models.CharField(max_length=24)
    surname = models.CharField(max_length=24)
    nick = models.CharField(max_length=24, blank=True, null=True)
    mail = models.CharField(max_length=24, blank=True, null=True)
    phone_tel = models.CharField(max_length=24, blank=True, null=True)
    desc = models.CharField(max_length=200, blank=True, null=True)
    race_licence = models.BooleanField()

    def __str__(self):
        return "{} {} ({})".format(self.name, self.surname, self.nick)


class Race(models.Model):
    name = models.CharField(max_length=256)
    place = models.CharField(max_length=256)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    finished = models.BooleanField(default=False)   # True id Race is finished
    race_type_choices = (
        ('TimeAttack', 'TimeAttack'),
        ('ShorthestSum', 'ShorthestSum')
        )

    race_type = models.CharField(
        choices=race_type_choices,
        default='TimeAttack',
        max_length=24
    )

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
    engine_model = models.CharField(max_length=24, blank=True, null=True)
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
        max_length=24,
        null=True
    )
    power = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)     # unit: Horse Power (KM)
    torque = models.DecimalField(decimal_places=0, max_digits=9, blank=True, null=True)     # unit: Nm
    engine_capacity = models.DecimalField(decimal_places=0, max_digits=9)   #unit: ccm
    wankel = models.BooleanField()
    hybrid = models.BooleanField()

    def __str__(self):
        return "{} {} {}".format(self.manufacurer, self.model, round(self.engine_capacity/1000, 1))


class Team(models.Model):
    start_no = models.DecimalField(decimal_places=0, max_digits=9)
    driver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='+',)
    navigator = models.ForeignKey(Person, on_delete=models.CASCADE,null=True,  blank=True, related_name='+',)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    tclass = models.ForeignKey(CarClass, on_delete=models.CASCADE, related_name='+', )

    def __str__(self):
        if self.navigator is not None:
            navigator = ", "+self.navigator.name[:1]+'.'+self.navigator.surname
        else:
            navigator = ""

        team_name = "{}.{}{}".format(
            self.driver.name[:1],
            self.driver.surname,
            navigator
            )
        return "{}: {}".format(self.start_no, team_name)


class Track(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name


class Lap(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    taryfa = models.BooleanField()  # true if "taryfa"
    fee = models.DecimalField(default=0, decimal_places=0, max_digits=9)   # fee in seconds
    start_time = models.TimeField(blank=True, null=True)
    stop_time = models.TimeField(blank=True, null=True)
    result = models.BigIntegerField()  #result in milliseconds

    @property
    def result_plus_fee(self):
        return self.result+(self.fee*1000)

    @property
    def result_taryfa_klasa(self):
        if self.taryfa is True:
            #150% best time in the same track and class
            best_result = Lap.objects.filter(track=self.track, taryfa=False, team__tclass=self.team.tclass).order_by('result')[0]  # best result
            return int(best_result.result*1.5)

    @property
    def result_taryfa_gen(self):
        if self.taryfa is True:
            # 150% best time in the same track. class doesn't matter
            best_result = \
            Lap.objects.filter(track=self.track, taryfa=False).order_by('result')[
                0]  # best result
            return int(best_result.result * 1.5)

    @property
    def final_result_klasa(self):   # diffrent alg in taryfa time computing in "klasyfikacja generalna" and "klasyfikacja klasowa"
        if self.taryfa is True:
            return self.result_taryfa_klasa
        else:
            return self.result_plus_fee

    @property
    def final_result_gen(self): # diffrent alg in taryfa time computing in "klasyfikacja generalna" and "klasyfikacja klasowa"
        if self.taryfa is True:
            return self.result_taryfa_gen
        else:
            return self.result_plus_fee

    def __str__(self):
        return "{}, {}".format(self.track, self.team)


