from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class GroupSuperUserTests(APITestCase):

    def setUp(self):
        Users.objects.create_superuser('wwwbn@uke.nee', 'wwwbn@uke.nee', 'QAZqaz!@#$%^&*()_+')
        self.client = APIClient()
        self.client.login(username='wwwbn@uke.nee', password='QAZqaz!@#$%^&*()_+')

    def tearDown(self):
        self.client.logout()

    def test_add_group(self):
        data = {'name': 'test'}
        data1 = {'name': 'test1'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/group/', data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rm_group(self):
        data = {'name': 'test'}
        resp = self.client.post('/group/', data, format='json')
        group_id = resp.data['result']['id']
        group_name = resp.data['result']['name']
        self.assertEqual(group_name, 'test')
        resp = self.client.delete('/group/{}/'.format(group_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_group(self):
        data = {'name': 'test'}
        data_upd = {'name': 'test_upd'}
        resp = self.client.post('/group/', data, format='json')
        group_id = resp.data['result']['id']
        group_name = resp.data['result']['name']
        self.assertEqual(group_name, 'test')
        self.client.put('/group/{}/'.format(group_id), data_upd, format='json')
        resp = self.client.get('/group/{}/'.format(group_id), format='json')
        self.assertEqual(resp.data['result']['name'], 'test_upd')

    def test_ls_group(self):
        data = {'name': 'test'}
        data1 = {'name': 'test1'}
        response = self.client.post('/group/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/group/', data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/group/', format='json')
        self.assertAlmostEqual(response.data['result'],
                               [{u'id': 1, 'name': u'test'},
                                {u'id': 2, 'name': u'test1'}])



