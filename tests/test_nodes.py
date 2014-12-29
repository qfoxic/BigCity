from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class NodeTests(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('wwwbnv@uke.nee', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def _createAndLoginUser(self, username):
        self.client.logout()
        data = {'username': username, 'email': username,
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
        response = self.client.get('/user/{}/groups/'.format(uid), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [i[0] for i in response.data['result']]

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

    def _removeNodes(self, *args):
        self.client.get('/logout/')
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        for i in args:
            response = self.client.delete('/node/{}/'.format(i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    #NODE REMOVAL with parent.
    # Remove simple node.
    # Access to nodes - change owner, change group.
    # Test sharing.
    def test_node_data(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        gids = self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid1, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertTrue(data['gid'] in gids)
        self.assertEqual(None, data['parent'])
        response = self.client.get('/node/{}/'.format(pid2), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid2, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertTrue(data['gid'] in gids)
        self.assertEqual(pid1, data['parent'])
        response = self.client.get('/node/{}/'.format(pid3), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['result']
        self.assertEqual(pid3, data['id'])
        self.assertEqual(uid, data['uid'])
        self.assertTrue(data['gid'] in gids)
        self.assertEqual(pid2, data['parent'])
        self._removeNodes(pid1, pid2, pid3)

    def test_node_path(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
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
        self._removeNodes(pid1, pid2, pid3)

    def test_update_node(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')
        self._removeNodes(pid1, pid2, pid3)

    def test_owner_read_perm(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_same_group_read_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_diff_group_read_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_same_group_read_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def test_diff_group_read_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee112')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def test_same_group_write_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_diff_group_write_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_same_group_write_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '555'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def test_diff_group_write_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '555'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/node/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def test_same_group_delete_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        for p in [pid1, pid2, pid3]:
            response = self.client.delete('/node/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_diff_group_delete_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        for p in [pid1, pid2, pid3]:
            response = self.client.delete('/node/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_same_group_delete_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '111'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid2, create=False)
        for p in [pid1]:
            response = self.client.delete('/node/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)

    def test_diff_group_delete_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.put('/node/{}/'.format(pid1), {'perm': '111'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        for p in [pid1]:
            response = self.client.delete('/node/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._removeNodes(pid1, pid2, pid3)














