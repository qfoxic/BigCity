from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.models import Users


class BaseAPITestCase(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('wwwbnv@uke.nee', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def _createAndLoginUser(self, username, groupname=None, **kwargs):
        self.client.logout()
        data = {'username': username, 'email': username,
                'phone': '1234567890', 'gender': 'm',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        data.update(kwargs)
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uid = response.data['result']['id']

        if groupname:
            self.client.login(username='wwwbnv@uke.nee', password='qwerty')
            grp_data = {'name': groupname}
            response = self.client.post('/group/', grp_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            gid = response.data['result']['id']
            response = self.client.post('/user/{}/updgroups/'.format(uid), {'gids': [{'id': gid}]}, format='json')
            self.client.logout()

        self._loginUser(username)
        return uid

    def _removeNodes(self, t, *args):
        self.client.get('/logout/')
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        for i in args:
            response = self.client.delete('/{}/{}/'.format(t, i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _loginUser(self, username):
        self.client.post('/login/', {'username': username,
                                     'password': '1234567890'},
                         format='json')

    def _createAndAddGroup(self, groupname, uid, create=True):
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        if create:
            grp_data = {'name': groupname}
            response = self.client.post('/group/', grp_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            gid = response.data['result']['id']
        else:
            response = self.client.get('/group/', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            res = response.data['result']
            gid = [d['id'] for d in res if d['name'] == groupname]
            gid = gid[0] if gid else -1
        response = self.client.post('/user/{}/addgroup/'.format(uid),
                                    {'gid': gid}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/{}/groups/'.format(uid), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        return [i['id'] for i in response.data['result']]
