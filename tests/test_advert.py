import datetime

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
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uid = response.data['result']['id']
        self.client.post('/login/', {'username': username,
                                     'password': '1234567890'},
                         format='json')
        return uid

    def _createTree(self, uid):
        cat1 = {'uid': uid, 'perm': '666', 'title': 'Category1'}
        response = self.client.post('/category/', cat1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid0 = response.data['result']['id']
        now_2 = datetime.datetime.now() + datetime.timedelta(days=2)
        now_1 = datetime.datetime.now() + datetime.timedelta(days=-1)
        pidcat = response.data['result']['id']
        node1 = {'uid': uid, 'perm': '666', 'title': 'Advert1', 'parent': pidcat,
            'country': 'Ukraine', 'city': 'Sambir',
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 100,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node2 = {'uid': uid, 'perm': '666', 'title': 'Advert2', 'parent': pidcat,
            'country': 'Ukraine', 'city': 'Lviv',
            'rooms': 2, 'square_gen': 80, 'square_live': 60,
            'room_height': 2, 'floors': 10, 'floor': 1, 'wall_type': 1,
            'build_type': 1, 'price': 120,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node3 = {'uid': uid, 'perm': '644', 'title': 'Advert3','parent': pidcat,
            'country': 'Ukraine', 'city': 'Kyiv',
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 110,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node4 = {'uid': uid, 'perm': '644', 'title': 'Advert4','parent': pidcat,
            'country': 'Ukraine', 'city': 'Donetsk',
            'rooms': 3, 'square_gen': 74, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 130,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node5 = {'uid': uid, 'perm': '600', 'title': 'Advert5','parent': pidcat,
            'country': 'Ukraine', 'city': 'Rivne',
            'rooms': 3, 'square_gen': 73, 'square_live': 60,
            'room_height': 2, 'floors': 4, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 150,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node6 = {'uid': uid, 'perm': '600', 'title': 'Advert6','parent': pidcat,
            'country': 'Ukraine', 'city': 'Dnipropetrovsk',
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 90,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        pids = []
        for node in [node1, node2, node3, node4]:
            response = self.client.post('/advert/', node, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            pids.append(response.data['result']['id'])
        response = self.client.post('/advert/', node5, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid2 = response.data['result']['id']
        response = self.client.post('/advert/', node6, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid3 = response.data['result']['id']
        return pids[0], pids[1], pids[2], pids[3], pid2, pid3, pid0

    def _removeNodes(self, t, *args):
        self.client.get('/logout/')
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        for i in args:
            response = self.client.delete('/{}/{}/'.format(t, i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_creation(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        self._removeNodes('advert',pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category',cat)

    def test_incorrect_parent_creation(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        cat1 = {'uid': uid, 'perm': '666', 'title': 'Category1'}
        response = self.client.post('/node/', cat1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat_id = response.data['result']['id']
        node = {'uid': uid, 'perm': '600', 'title': 'Advert6','parent': cat_id,
            'country': 'Ukraine', 'city': 'Dnipropetrovsk',
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 90,
            'text': 'Hello this is me'}
        response = self.client.post('/advert/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self._removeNodes('node', cat_id)

    # Test location.
    def test_update_advert_node(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.put('/advert/{}/'.format(pid1),
                                   {'perm': '777', 'title': 'test1',
                                    'finished': '2005-12-12 12:12:12'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/advert/{}/'.format(pid1), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')
        self.assertEqual(response.data['result']['title'], 'test1')
        self.assertEqual(response.data['result']['finished'], '2005-12-12 12:12:12')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_finished_adverts_list(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'where': '(finished is null or finished > "{}")'.format(datetime.datetime.now())},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_nearest_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'search': 'near', 'lon': 24.03, 'lat': 49.85},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['city'] in ['Lviv', 'Kyiv'])
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_within_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'search': 'within', 'lon':23.20, 'lat': 49.51, 'radius': 0.9},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'])
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_city_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'search': 'city', 'cities': 'Lviv,Sambir'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_country_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'search': 'country', 'countries': 'Ukraine'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_price_order_asc(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'order': 'price'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '100.00')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_price_order_desc(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'order': '-price'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '120.00')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_price_gt(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'price': 'gt110.0'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '120.00')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)

    def test_price_lt(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/adverts/{}/'.format(cat),
            {'price': 'lt110.0'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '100.00')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
