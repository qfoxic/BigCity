from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
setup_test_environment()

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
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.get('/user/{}/'.format(user_id), format='json')
        data = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['resume'], 'super_file')
        self.assertEqual(data['email'], 'wwww@www.www')

    def test_incorrect_add_user(self):
        data = {'username': 'test', 'email': 'wwwwww',
                'last_name': 'tetete', 'resume': 'super_file'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found(self):
        response = self.client.get('/user/{}/'.format(123), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_correct_update_user(self):
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        data = {'email': 'ww1@www.www', 'resume': 'test2', 'id': user_id}
        response = self.client.put('/user/{}/'.format(user_id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/'.format(user_id), format='json')
        data = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['resume'], 'test2')
        self.assertEqual(data['email'], 'ww1@www.www')
        self.assertEqual(data['first_name'], 'tets')

    def test_incorrect_update_user(self):
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        data = {'email': 'ww1www.www', 'resume': 'test2', 'id': user_id}
        response = self.client.put('/user/{}/'.format(user_id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_existing_add_group(self):
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        udata = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', udata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/groups/'.format(user_id),
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['result'][0][0], gid)

    def test_inexisted_add_group(self):
        gid = 123
        udata = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', udata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rm_group(self):
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        udata = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', udata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/groups/'.format(user_id),
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['result'][0][0], gid)
        response = self.client.post('/user/{}/rmgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/groups/'.format(user_id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data['result']), [])

    def test_login(self):
        self.client.logout()
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post('/login/', {'username': 'teste',
                                                'password': 'qwerty'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_login(self):
        self.client.logout()
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post('/login/', {'username': 'teste',
                                                'password': 'qwer'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ch_password(self):
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        self.client.logout()
        response = self.client.post('/login/', {'username': 'test',
                                                'password': '1234567890'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/user/{}/chpasswd/'.format(user_id),
                                    {'password': 'qwerty'},
                                    format='json')
        self.client.logout()
        response = self.client.post('/login/', {'username': 'test',
                                                'password': 'qwerty'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


