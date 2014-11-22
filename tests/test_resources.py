from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class ResourceTests(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('teste', 'wwwbnv@uke.nee', 'qwerty')
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

    def _createAndAddGroup(self, groupname, uid, create=True):
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
        return gid

    def _createTree(self, uid):
        node = {'uid': uid, 'perm': '666'}
        response = self.client.post('/node/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid = response.data['result']['id']
        node = {'uid': uid, 'perm': '666', 'parent': pid}
        response = self.client.post('/node/', node, format='json')
        pid2 = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return pid, pid2

    def _removeNodes(self, *args):
        self.client.get('/logout/')
        self.client.login(username='teste', password='qwerty')
        for i in args:
            response = self.client.delete('/node/{}/'.format(i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_create_correct_parent(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid1, data['parent']['id'])
        self._removeNodes(pid1, pid2)

    def test_resource_create_incorrect_parent(self):
        self._createAndLoginUser('user')
        response = self.client.post('/resource/',
                                    {'parent': '54704556e1382314feaea1ab'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_permissions_same_group(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        uid1 = self._createAndLoginUser('user1')
        self._createAndAddGroup('test', uid1, False)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid1, data['parent']['id'])
        self._removeNodes(pid1, pid2)

    def test_permissions_diff_group_allow(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        uid1 = self._createAndLoginUser('user1')
        self._createAndAddGroup('test1', uid1)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2)

    def test_permissions_diff_group_deny(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uid1 = self._createAndLoginUser('user1')
        self._createAndAddGroup('test1', uid1)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2)

    def test_data_id_perms_allow(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_id = response.data['result']['id']
        response = self.client.get('/resource/{}/'.format(res_id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2)

    def test_data_id_perms_deny(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        res_id = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/resource/{}/'.format(res_id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2)

    def test_data_tag_perms_allow(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reso_id = response.data['result']['id']
        response = self.client.get('/node/{}/reso_by_tag/'.format(pid1),
                                   {'tag': 'resource'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['id'], reso_id)
        self._removeNodes(pid1, pid2)

    def test_data_tag_perms_deny(self):
        uid = self._createAndLoginUser('user')
        self._createAndAddGroup('test', uid)
        pid1, pid2 = self._createTree(uid)
        response = self.client.post('/resource/',
                                    {'parent': pid1}, format='json')
        res_id = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/resource/{}/'.format(res_id),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2)

