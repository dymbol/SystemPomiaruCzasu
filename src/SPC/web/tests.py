from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from web.models import *


class TestSites(TestCase):
    """Testing if subsites works"""
    def setUp(self):
        user = User.objects.create_user('temporary', 'tmp@tmp.pl', 'temp')
        race = Race.objects.create(name="test_race",
                    start_date = datetime.now(),
                    end_date = datetime.now(),
                    place="test_place",
                    finished=True,
                    race_type="TimeAttack")
        person = Person.objects.create(name="test_person",
                        surname="test_sur",
                        nick="test_nick",
                        race_licence = False)
        car = Car.objects.create(manufacurer="Ford",
                  model="GT",
                  desc="xxx",
                  fuel="gasoline",
                  engine_capacity=1300,
                  wankel=False,
                  hybrid=False
                  )
        klasa = CarClass.objects.create(name="test_klass",
                         type="Capacity",
                         cap_min=1000,
                         cap_max=2000)
        Team.objects.create(start_no=1,
                    driver=person,
                    race=race,
                    car=car,
                    tclass=klasa)


    def test_secure_page(self):
        print("======= BASIC SITE TESTING MODULE =======")
        self.client.login(username="temporary", password="temporary")
        sites = ['/',
                 '/race/choose/1',
                 '/team/list',
                 '/results',
                 '/result/register',
                 '/change_track/1',
                 '/time_meter/1',
                 ]
        for site in sites:
            print("Testing '{}' site".format(site))
            response = self.client.get(site, follow=True)
            print(response)
            self.assertEqual(response.status_code, 200)
