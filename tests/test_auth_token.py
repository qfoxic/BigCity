from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AuthTokenTests(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('wwwbnv@uke.nee', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_get_token(self):
        self.client.logout()
        data = {'username': 'wwwbnv@uke.nee', 'password': 'qwerty'}
        response = self.client.post('/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['token']
        self.assertTrue(token)

