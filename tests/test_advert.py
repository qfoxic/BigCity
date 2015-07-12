import datetime

from users.models import Users

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


def createTestData():
    import random
    client = APIClient()
    user = {'username': 'test@testovich.com', 'email': 'test@testovich.com',
                'first_name': 'tets', 'last_name': 'tetete',
                'resume': 'super_file', 'password': '1234567890'}
    response = client.post('/user/', user, format='json')
    uid = response.data['result']['id']
    client.post('/login/', {'username': 'test@testovich.com',
                            'password': '1234567890'},
                         format='json')
    client.login(username='test@testovich.com', password='qwerty')
    categories = [
        {'uid': uid, 'perm': '666', 'title': 'Automobiles',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'Audi'},
            {'uid': uid, 'perm': '666', 'title': 'Skoda'},
            {'uid': uid, 'perm': '666', 'title': 'BMW'},
            {'uid': uid, 'perm': '666', 'title': 'Opel'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Buildings',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'New'},
            {'uid': uid, 'perm': '666', 'title': 'Secondary'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Books',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'Shevchenko'},
            {'uid': uid, 'perm': '666', 'title': 'Franko'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'School',
                 'sub': [
            {'uid': uid, 'perm': '666', 'title': 'High School'},
            {'uid': uid, 'perm': '666', 'title': 'Middle'},
            {'uid': uid, 'perm': '666', 'title': 'Colledge'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Sport',
                 'sub': [
            {'uid': uid, 'perm': '666', 'title': 'Aikido'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Trips',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'Ukraine'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Cities',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'London'},
            {'uid': uid, 'perm': '666', 'title': 'Kyiv'},
            {'uid': uid, 'perm': '666', 'title': 'Paris'},
            {'uid': uid, 'perm': '666', 'title': 'Sambir'},
            ]},
        {'uid': uid, 'perm': '666', 'title': 'Companies',
         'sub': [
            {'uid': uid, 'perm': '666', 'title': 'NIX'},
            {'uid': uid, 'perm': '666', 'title': 'EPAM'},
            {'uid': uid, 'perm': '666', 'title': 'Google'},
            {'uid': uid, 'perm': '666', 'title': 'Microsoft'},
            ]},
    ]
    pidcats = []
    print 'Generating categories'
    for c in categories:
        resp = client.post('/category/', c, format='json')
        print resp
        pidcat = resp.data['result']['id']
        pidcats.append(pidcat)
        for s in c['sub']:
            s['parent'] = pidcat
            resp = client.post('/category/', s, format='json')
            subpidcat = resp.data['result']['id']
            pidcats.append(subpidcat)

    print 'Generating adverts'
    locations = [{'country': 'Ukraine', 'city': 'Sambir', 'loc': (23.1968986,49.522311)},
                 {'country': 'Ukraine', 'city': 'Sambir', 'loc': (23.1968912,49.522300)},
                 {'country': 'Ukraine', 'city': 'Lviv', 'loc': (24.0122356,49.8326891)},
                 {'country': 'Ukraine', 'city': 'Kyiv', 'loc': (30.5326905, 50.4020355)},
                 {'country': 'Ukraine', 'city': 'Donetsk', 'loc': (37.7615206, 47.9901174)},
                 {'country': 'Ukraine', 'city': 'Rivne', 'loc': (26.2652575,50.6191895)},
                 {'country': 'Ukraine', 'city': 'Rivne', 'loc': (26.265258,50.619188)},
                 {'country': 'Ukraine', 'city': 'Dnipropetrovsk', 'loc': (35.0003565,48.4622985)},
                 {'country': 'Ukraine', 'city': 'Dnipropetrovsk', 'loc': (35.0003569,48.4622785)}]

    data = {'uid': None, 'perm': '666', 'title': 'Advert1', 'parent': None,
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': None,
            'text': 'Hello this is a super randomly generated advert'}
    texts = [
             '''He was found guilty of bribery, abuse of power and "intentionally disclosing
                national secrets", China's official Xinhua news agency reports.
                Until his retirement in 2012, Zhou was one of China's most powerful men.
                He was put under investigation one year later as part of President Xi
                Jinping's major anti-corruption campaign.
                State TV showed a clip of Zhou, 72, pleading guilty at a closed-door trial in
                the northern city of Tianjin. When responding to the judge, he said he would not
                launch an appeal. "I've realised the harm I've caused to the party and the people.
                I plead guilty and I regret my crimes," he said.''',
                '''After all, Zhou Yongkang had held a seat at the very top of the Chinese
                government pyramid. If he was thoroughly corrupt, some in China might ask whether
                others at the top were rotten too.
                In the end, the decision to keep Zhou Yongkang's trial secret matches the case
                surrounding him, and Zhou's own public persona: inaccessible and secretive.
                ''',
                '''has been welcoming of the conviction, with one user commenting: "Haha! Put the
                old tiger in the cage!"
                The jibe is a reference to President Xi Jinping's promise to crack down on both
                "tigers and flies" - meaning officials at all levels - in his fight against
                corruption.
                Zhou was charged in April, nine months after a formal investigation was announced.
                He has since been expelled from the Communist Party.
                '''
                ]
    for _ in xrange(0, 50000):
        data.update(random.choice(locations))
        data['parent'] = random.choice(pidcats)
        data['price'] = round(float(random.triangular(100, 1000)),2)
        data['uid'] = random.randint(1, 50)
        data['text'] = random.choice(texts)
        data['title'] = 'Some title '+ data['parent']
        data['rooms'] = random.randint(1, 4)
        data['square_gen'] = random.randint(30, 100)
        data['square_live'] = data['square_gen'] - random.randint(10, 15)
        data['room_height'] = round(float(random.triangular(1, 4)),2)
        data['floor'] = random.randint(1, 9)
        client.post('/advert/', data, format='json')


def addImagesToAdvert(pid='5579d77ee138235570a06774', uid=2):
    client = APIClient()
    client.post('/login/', {'username': 'test@testovich.com',
                            'password': '1234567890'},
                         format='json')
    with open('tests/test.jpg') as f:
        asset = {'uid': uid, 'perm': '666', 'parent': pid,
                 'title': 'Image 01', 'asset_type': 'image',
                 'content_type': 'image/jpg', 'content': f}
        client.post('/image/', asset)


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
            'country': 'Ukraine', 'city': 'Sambir', 'loc': (23.1968986,49.522311),
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 100,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node2 = {'uid': uid, 'perm': '666', 'title': 'Advert2', 'parent': pidcat,
            'country': 'Ukraine', 'city': 'Lviv', 'loc': (24.0122356,49.8326891),
            'rooms': 2, 'square_gen': 80, 'square_live': 60,
            'room_height': 2, 'floors': 10, 'floor': 1, 'wall_type': 1,
            'build_type': 1, 'price': 120,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node3 = {'uid': uid, 'perm': '644', 'title': 'Advert3','parent': pidcat,
            'country': 'Ukraine', 'city': 'Kyiv', 'loc': (30.5326905, 50.4020355),
            'rooms': 3, 'square_gen': 70, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 110,
            'finished': now_2.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node4 = {'uid': uid, 'perm': '644', 'title': 'Advert4','parent': pidcat,
            'country': 'Ukraine', 'city': 'Donetsk', 'loc': (37.7615206, 47.9901174),
            'rooms': 3, 'square_gen': 74, 'square_live': 60,
            'room_height': 2, 'floors': 9, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 130,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node5 = {'uid': uid, 'perm': '600', 'title': 'Advert5','parent': pidcat,
            'country': 'Ukraine', 'city': 'Rivne', 'loc': (26.2652575,50.6191895),
            'rooms': 3, 'square_gen': 73, 'square_live': 60,
            'room_height': 2, 'floors': 4, 'floor': 2, 'wall_type': 1,
            'build_type': 1, 'price': 150,
            'finished': now_1.strftime('%Y-%m-%d %H:%M:%S'),
            'text': 'Hello this is me'}
        node6 = {'uid': uid, 'perm': '600', 'title': 'Advert6','parent': pidcat,
            'country': 'Ukraine', 'city': 'Dnipropetrovsk', 'loc': (35.0003565,48.4622985),
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
            'text': 'Hello this is myself'}
        response = self.client.post('/advert/', node, format='json')
        self._removeNodes('node', cat_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_advert_node(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.put('/advert/{}/'.format(pid1),
                                   {'perm': '777', 'title': 'test1',
                                    'finished': '2005-12-12 12:12:12'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/advert/{}/'.format(pid1), format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')
        self.assertEqual(response.data['result']['title'], 'test1')
        self.assertEqual(response.data['result']['finished'], '2005-12-12 12:12:12')

    def test_finished_adverts_list(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/', format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_nearest_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'table': 'nearest', 'tparams':'lon=24.03,lat=49.85'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['city'] in ['Lviv', 'Kyiv'])

    def test_within_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'table': 'within', 'tparams': 'lon=23.20,lat=49.51,radius=0.9'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'])

    def test_city_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'where': 'city in ("Lviv","Sambir")'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_country_location(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'where': 'country in ("Ukraine")'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_price_order_asc(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'order': 'price'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '100.00')

    def test_price_order_desc(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/'.format(cat),
            {'order': '-price'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '120.00')

    def test_price_gt(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/',
            {'where': 'price > 110.0'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '120.00')

    def test_price_lt(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        pid1, pid2, pid3, pid4, pid5, pid6, cat = self._createTree(uid)
        response = self.client.get('/nodes/advert/'.format(cat),
            {'where': 'price < 110.0'},
            format='json')
        self._removeNodes('advert', pid1, pid2, pid3, pid4, pid5, pid6)
        self._removeNodes('category', cat)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], 'uid.00')
