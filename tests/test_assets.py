import datetime

from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AssetTests(APITestCase):
    def setUp(self):
        Users.objects.create_superuser('wwwbnv@uke.nee', 'wwwbnv@uke.nee', 'qwerty')
        self.client = APIClient()
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')

    def tearDown(self):
        self.client.logout()

    def _createUser(self, username):
        self.client.logout()
        data = {'username': username, 'email': username,
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uid = response.data['result']['id']
        return uid

    def _loginUser(self, username):
        self.client.post('/login/', {'username': username,
                                     'password': '1234567890'},
                         format='json')

    def _createTree(self, uid):
        node = {'uid': uid, 'perm': '666', 'title': 'Category1'}
        response = self.client.post('/category/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cat = response.data['result']['id']
        now_1 = datetime.datetime.now() + datetime.timedelta(days=2)
        node = {'uid': uid, 'perm': '600', 'title': 'Advert6','parent': cat,
            'country': 'Ukraine', 'city': 'Dnipropetrovsk',
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 90,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        response = self.client.post('/advert/', node, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pid = response.data['result']['id']
        with open('tests/test.jpg') as f:
            asset = {'uid': uid, 'perm': '666', 'parent': pid,
                     'title': 'Image', 'asset_type': 'image',
                     'content_type': 'image/jpg', 'content': f}
            response = self.client.post('/image/', asset)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            aid = response.data['result']['id']
        return cat, pid, aid

    def _removeNodes(self, t, *args):
        self.client.get('/logout/')
        self.client.login(username='wwwbnv@uke.nee', password='qwerty')
        for i in args:
            response = self.client.delete('/{}/{}/'.format(t, i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_node_data(self):
        uid = self._createUser('wwwbnv@uke.nee1')
        self._loginUser('wwwbnv@uke.nee1')
        cat, _, _ = self._createTree(uid)
        #self._removeNodes('category', cat)

