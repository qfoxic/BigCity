from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
setup_test_environment()

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class NodeTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser('teste', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='teste', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def test_correct_add_node_wo_parent(self):
        self.client.logout()
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        uid = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/login/', {'username': 'test',
                                                'password': '1234567890'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(uid),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = {'uid': uid, 'perm': '666'}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_add_node_parent(self):
        self.client.logout()
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        uid = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/login/', {'username': 'test',
                                                'password': '1234567890'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(uid),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = {'uid': uid, 'perm': '666'}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pid = response.data['result']['id']
        node = {'uid': uid, 'perm': '666', 'parent': self.pid}
        response = self.client.post('/node/', node, format='json')
        self.pid2 = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_update_node(self):
        self.client.logout()
        data = {'username': 'test', 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        uid = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/login/', {'username': 'test',
                                                'password': '1234567890'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'name': 'test'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gid = response.data['result']['id']
        response = self.client.post('/user/{}/addgroup/'.format(uid),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = {'uid': uid, 'perm': '666'}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        nid = response.data['result']['id']
        node = {'perm': '777'}
        response = self.client.put('/node/{}/'.format(nid),
                                   node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
