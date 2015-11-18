from rest_framework import status
from tests.common import BaseAPITestCase


class MessageTests(BaseAPITestCase):
    def test_message_creation(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message'}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._removeNodes('message', mid)

    def test_update_message(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message'}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        response = self.client.put('/message/{}/'.format(mid),
                                   {'perm': '777', 'title': 'test1'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/message/{}/'.format(mid), format='json')
        self._removeNodes('message', mid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['perm'], '777')
        self.assertEqual(response.data['result']['title'], 'test1')

    def test_message_visibility_in_a_group_deny(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message'}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12', 'other')
        response = self.client.get('/message/{}/'.format(mid), format='json')
        self.assertEqual(response.status_code, 401)
        self._removeNodes('message', mid)

    def test_message_visibility_in_a_group_allow(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message'}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        response = self.client.get('/message/{}/'.format(mid), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result']['title'], msg1['title'])
        self._removeNodes('message', mid)

    def test_list_message_shared_in_the_same_country(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11', country='ukraine', city='lviv', state='lvivska')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'ukraine-lvivska-lviv', 'body': 'My super message',
                'country': 'ukraine', 'region': 'lvivska', 'city': 'lviv'}
        msg2 = {'uid': uid, 'perm': '640', 'title': 'ua-kyiv-kyiv', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska', 'city': 'kyiv'}
        msg3 = {'uid': uid, 'perm': '640', 'title': 'ua-lvivska', 'body': 'My super message',
                'country': 'ukraine', 'region': 'lvivska'}
        msg5 = {'uid': uid, 'perm': '640', 'title': 'usa', 'body': 'My super message',
                'country': 'usa'}
        msg4 = {'uid': uid, 'perm': '640', 'title': 'ua', 'body': 'My super message',
                'country': 'ukraine'}
        msg6 = {'uid': uid, 'perm': '640', 'title': 'ua-kyiv', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska'}
        mids = []
        for m in [msg1, msg2, msg3, msg4, msg5, msg6]:
            response = self.client.post('/message/', m, format='json')
            self.assertEqual(response.status_code, 200)
            mids.append(response.data['result']['id'])

        self._createAndLoginUser('wwwbnv@uke.nee12')
        response = self.client.get(
            '/nodes/message/',
            {'tparams': 'country=ukraine,region=lvivska,city=lviv'},
            format='json'
        )
        self._removeNodes('message', *mids)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)

    def test_list_message_shared_in_the_same_state(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11', country='ukraine', city='lviv', state='lvivska')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message',
                'country': 'ukraine', 'region': 'lvivska', 'city': 'lviv'}
        msg2 = {'uid': uid, 'perm': '640', 'title': 'Message2', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska', 'city': 'kyiv'}
        msg3 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine'}
        msg5 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'usa'}
        msg4 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine', 'region': 'lvivska'}
        msg6 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska'}
        mids = []
        for m in [msg1, msg2, msg3, msg4, msg5, msg6]:
            response = self.client.post('/message/', m, format='json')
            self.assertEqual(response.status_code, 200)
            mids.append(response.data['result']['id'])

        self._createAndLoginUser('wwwbnv@uke.nee12')
        response = self.client.get(
            '/nodes/message/',
            {'tparams': 'country=ukraine,region=lvivska,city=sambir'},
            format='json'
        )
        self._removeNodes('message', *mids)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_list_message_shared_in_the_same_city(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11', country='ukraine', city='lviv', state='lvivska')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message',
                'country': 'ukraine', 'region': 'lvivska', 'city': 'lviv'}
        msg2 = {'uid': uid, 'perm': '640', 'title': 'Message2', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska', 'city': 'kyiv'}
        msg3 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine', 'region': 'yivska'}
        msg5 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'usa'}
        msg4 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine', 'region': 'vivska'}
        msg6 = {'uid': uid, 'perm': '640', 'title': 'Message3', 'body': 'My super message',
                'country': 'ukraine', 'region': 'kyivska'}
        mids = []
        for m in [msg1, msg2, msg3, msg4, msg5, msg6]:
            response = self.client.post('/message/', m, format='json')
            self.assertEqual(response.status_code, 200)
            mids.append(response.data['result']['id'])

        self._createAndLoginUser('wwwbnv@uke.nee12')
        response = self.client.get('/nodes/message/', {'tparams': 'country=ukraine,region=lvivska,city=lviv'},
                                   format='json')
        self._removeNodes('message', *mids)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_list_message_shared_to_uids_incorrect(self):
        uid = self._createAndLoginUser('wwwbnv@uke.nee11', country='ukraine', city='lviv', state='lvivska')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message',
                'country': 'usa', 'region': 'lvivska', 'city': 'lviv', 'shared': [123]}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        self.assertEqual(response.status_code, 200)
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        response = self.client.get('/nodes/message/',
                                   {'tparams': 'country=ukraine,region=lvivska,city=lviv'},
                                   format='json')
        self._removeNodes('message', mid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_list_message_shared_to_uids_correct(self):
        uid2 = self._createAndLoginUser('wwwbnv@uke.nee12')
        uid = self._createAndLoginUser('wwwbnv@uke.nee11', country='ukraine', city='lviv', state='lvivska')
        msg1 = {'uid': uid, 'perm': '640', 'title': 'Message1', 'body': 'My super message',
                'country': 'usa', 'region': 'lvivska', 'city': 'lviv', 'shared': [uid2]}
        response = self.client.post('/message/', msg1, format='json')
        mid = response.data['result']['id']
        self.assertEqual(response.status_code, 200)
        self._loginUser('wwwbnv@uke.nee12')
        response = self.client.get('/nodes/message/',
                                   {'tparams': 'country=ukraine,region=lvivska,city=lviv'},
                                   format='json')
        self._removeNodes('message', mid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
