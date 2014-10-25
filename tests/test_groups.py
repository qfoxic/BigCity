from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.login(username='vpaslav', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)