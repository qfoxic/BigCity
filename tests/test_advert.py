from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AdvertTests(APITestCase):
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
        return gid

    def _createTree(self, uid):
        node = {'uid': uid, 'perm': '666', 'title': 'Advert1'}
        response = self.client.post('/advert/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid = response.data['result']['id']
        node = {'uid': uid, 'perm': '666', 'parent': pid, 'title': 'Advert2'}
        response = self.client.post('/advert/', node, format='json')
        pid2 = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        node = {'uid': uid, 'perm': '666', 'parent': pid2, 'title': 'Advert3'}
        response = self.client.post('/advert/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid3 = response.data['result']['id']
        address = {'country': 'Ukraine', 'region': 'Lviv', 'city': 'Lviv',
                   'street': 'Mazepy 24', 'parent': pid, 'kind': 'address'}
        response = self.client.post('/address/', address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rdata = response.data['result']
        self.assertEqual(rdata['region'], 'Lviv')
        self.assertEqual(rdata['city'], 'Lviv')
        price = {'price': 12.23, 'duration': 81400, 'parent': pid}
        response = self.client.post('/price/', price, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rdata = response.data['result']
        self.assertEqual(rdata['price'], 12.23)
        self.assertEqual(rdata['duration'], 81400)
        poster = {'title': 'SOME TITLE', 'text': 'SOME TEXT', 'parent': pid}
        response = self.client.post('/poster/', poster, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rdata = response.data['result']
        self.assertEqual(rdata['title'], 'SOME TITLE')
        self.assertEqual(rdata['text'], 'SOME TEXT')
        building = {'rooms': 1, 'square_gen': 12, 'square_live': 23,
                    'room_height': 2, 'floors': 12, 'floor': 3, 'wall_type': 1,
                    'build_type': 1, 'parent': pid}
        response = self.client.post('/building/', building, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rdata = response.data['result']
        self.assertEqual(rdata['rooms'], 1)
        self.assertEqual(rdata['build_type'], 1)
        return pid, pid2, pid3

    def _removeNodes(self, *args):
        self.client.get('/logout/')
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        for i in args:
            response = self.client.delete('/advert/{}/'.format(i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_advert_creation(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        self._removeNodes(pid1, pid2, pid3)

    # Test assign category to advert.
    # Test resource removal.
    # Test resource update.
    # Test list resources.
    # Test list of multiple resources.

    def test_update_advert_node(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.put('/advert/{}/'.format(pid1),
                                   {'perm': '777', 'title': 'test1'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/advert/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')
        self.assertEqual(response.data['result']['title'], 'test1')
        self._removeNodes(pid1, pid2, pid3)

    def test_get_advert_resources(self):
        uid = self._createAndLoginUser('wwwbnv@uke1111.nee')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/advert/{}/resources/'.format(pid1),
                                   {'kind': 'price'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['duration'], 81400)
        rid = response.data['result'][0]['id']
        response = self.client.get('/advert/{}/resources/'.format(pid1),
                                   {'rid': rid}, format='json')
        response = self.client.get('/advert/{}/resources/'.format(pid1),
                                   {'kind': 'address'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['city'], 'Lviv')
        rid = response.data['result'][0]['id']
        response = self.client.get('/advert/{}/resources/'.format(pid1),
                                   {'kind': 'poster'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['text'], 'SOME TEXT')
        self._removeNodes(pid1, pid2, pid3)

    def test_get_multiple_resources_of_the_same_kind(self):
        uid = self._createAndLoginUser('wwwbnv@uke1111.nee')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        price = {'price': 12.3, 'duration': 8140, 'parent': pid1}
        response = self.client.post('/price/', price, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/advert/{}/resources/'.format(pid1),
                                   {'kind': 'price'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = response.data['result']
        for price in prices:
            self.assertTrue(price['price'] in [12.3, 12.23])
        self._removeNodes(pid1, pid2, pid3)

    def est_same_group_read_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)

    def est_diff_group_read_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '222'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)

    def est_same_group_read_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def est_diff_group_read_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '777'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def est_same_group_write_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)

    def est_diff_group_write_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '444'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)

    def est_same_group_write_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '555'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def est_diff_group_write_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '555'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        response = self.client.get('/category/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes(pid1, pid2, pid3)

    def est_same_group_delete_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        for p in [pid1, pid2, pid3]:
            response = self.client.delete('/category/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def est_diff_group_delete_perm_access(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        for p in [pid1, pid2, pid3]:
            response = self.client.delete('/category/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def est_same_group_delete_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '111'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test', uid2, create=False)
        for p in [pid1]:
            response = self.client.delete('/category/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)

    def est_diff_group_delete_perm_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee1')
        self._createAndAddGroup('test', uid)
        pid1, pid2, pid3 = self._createTree(uid)
        response = self.client.put('/category/{}/'.format(pid1), {'perm': '111'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.get('/logout/')
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        self._createAndAddGroup('test1', uid2)
        for p in [pid1]:
            response = self.client.delete('/category/{}/'.format(p))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self._removeNodes(pid1, pid2, pid3)














