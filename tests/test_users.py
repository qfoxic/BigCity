from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class UserTests(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('wwwbnv@uke.nee', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_correct_add_user(self):
        self.client.logout()
        data = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.get('/user/{}/'.format(user_id), format='json')
        data = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['resume'], 'super_file')
        self.assertEqual(data['email'], 'wwww@www.www')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_add_user(self):
        data = {'username': 'test', 'email': 'wwwwww',
                'last_name': 'tetete', 'resume': 'super_file'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found(self):
        response = self.client.get('/user/{}/'.format(123), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_correct_update_user(self):
        data = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
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
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_update_user(self):
        data = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        data = {'email': 'ww1www.www', 'resume': 'test2', 'id': user_id}
        response = self.client.put('/user/{}/'.format(user_id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_existing_add_group(self):
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        udata = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', udata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/groups/'.format(user_id),
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['result'][0][0], gid)
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inexisted_add_group(self):
        gid = 123
        udata = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', udata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(user_id),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rm_group(self):
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        udata = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                 'first_name': 'tets', 'last_name': 'tetete',
                 'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', udata, format='json')
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
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        self.client.get('/logout/')
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post('/login/', {'username': 'wwwbnv@uke.nee',
                                                'password': 'qwerty'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_login(self):
        self.client.get('/logout/')
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post('/login/', {'username': 'wwwbnv@uke.nee',
                                                'password': 'qwer'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ch_password(self):
        data = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': 'QAZqaz1983'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        self.client.get('/logout/')
        response = self.client.post('/login/', {'username': 'wwww@www.www',
                                                'password': 'QAZqaz1983'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/user/{}/chpasswd/'.format(user_id),
                                    {'password': 'QAZQAZ1983'},
                                    format='json')
        self.client.get('/logout/')
        response = self.client.post('/login/', {'username': 'wwww@www.www',
                                                'password': 'QAZQAZ1983'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.login(email='wwwbnv@uke.nee', password='qwerty')
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rm_user(self):
        data = {'username': 'wwww@www.www', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_id = response.data['result']['id']
        response = self.client.delete('/user/{}/'.format(user_id),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

