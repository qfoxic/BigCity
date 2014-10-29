from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
setup_test_environment()

from mongoengine import connect
client = connect('test_city')

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

class UserTests(APITestCase):

    def setUp(self):
        User.objects.create_superuser('teste', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='teste', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_correct_add_user(self):
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.get('/user/{}/'.format(user_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

