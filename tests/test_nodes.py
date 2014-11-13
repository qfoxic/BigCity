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

    def _createAndLoginUser(self, username):
        self.client.logout()
        data = {'username': username, 'email': 'wwww@www.www',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uid = response.data['result']['id']
        self.client.post('/login/', {'username': username,
                                     'password': '1234567890'},
                         format='json')
        return uid

    def _createAndAddGroup(self, groupname, uid, add=True):
        if add:
            grp_data = {'name': groupname}
            response = self.client.post('/group/', grp_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            gid = response.data['result']['id']
        else:
            response = self.client.get('/group/', grp_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            gid = response.data['result'][0]['id']
        response = self.client.post('/user/{}/addgroup/'.format(uid),
                                    {'gid': gid}, format='json')

    def _createTree(self, uid):
        node = {'uid': uid, 'perm': '666'}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid = response.data['result']['id']
        node = {'uid': uid, 'perm': '666', 'parent': pid}
        response = self.client.post('/node/', node, format='json')
        pid2 = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = {'uid': uid, 'perm': '666', 'parent': pid2}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid3 = response.data['result']['id']
        return pid, pid2, pid3

    #NODE REMOVAL with parent.
    # Update node.
    # Remove simple node.
    # Access to nodes - change owner, change permissions, change group.
    # List access to nodes. - group perms.
    # Test sharing.
    def test_node_data(self):
        uid = self._createAndLoginUser('user')
        gid = self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid1, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertEqual([gid], data['access_level'])
        self.assertEqual(None, data['parent'])
        response = self.client.get('/node/{}/'.format(pid2), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid2, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertEqual([gid], data['access_level'])
        self.assertEqual(pid1, data['parent'])
        response = self.client.get('/node/{}/'.format(pid3), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid3, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertEqual([gid], data['access_level'])
        self.assertEqual(pid2, data['parent'])

    def test_node_path(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid1, data['path'])
        response = self.client.get('/node/{}/'.format(pid2), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual('{}.{}'.format(pid1, pid2), data['path'])
        response = self.client.get('/node/{}/'.format(pid3), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual('{}.{}.{}'.format(pid1, pid2, pid3), data['path'])

    def test_update_node(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, _, _ = self._createTree(uid, 'test')
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')

    def test_owner_read_perm(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, _, _ = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_same_group_read_perm(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, _, _ = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('user1')
        self._createAndAddGroup('test', uid)
        _, _, pid1, _, _ = self._createTree(uid2, 'test', False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_diff_group_read_perm(self):
        uid = self._createAndLoginUser('user')['id']
        _, _, pid1, _, _ = self._createTree(uid, 'test')
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('user1')['id']
        _, _, pid1, _, _ = self._createTree(uid2, 'test', False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


































