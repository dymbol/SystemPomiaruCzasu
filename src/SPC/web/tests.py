from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class TestSites(TestCase):
    '''Testing if subsites works'''
    def setUp(self):
        user = User.objects.create_user('temporary', 'tmp@tmp.pl', 'temp')
    def test_secure_page(self):
        print("======= BASIC SITE TESTING MODULE =======")
        self.client.login(username="temporary", password="temporary")
        sites = ['',
                 'race/choose/1',
                 'team/list',
                 'results',
                 'result/register',
                 'change_track/1',
                 'time_meter/1',
                 ]
        for site in sites:
            print("Testing '{}' site".format(site))
            response = self.client.get('/web/{}'.format(site), follow=True)
            self.assertEqual(response.status_code, 200)
