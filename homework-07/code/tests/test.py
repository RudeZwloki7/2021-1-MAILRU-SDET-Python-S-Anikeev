import json
import settings
from mock.flask_mock import SURNAME_DATA
from http_socket.client import HttpClient
from tests.base import TestBase

url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'
client = HttpClient()


class TestGetRequest(TestBase):
    def test_get_user_surname(self):
        user = self.builder.create_user()
        SURNAME_DATA[user.name] = user.surname
        resp = client.get_user_surname(user.name)

        assert resp['body'] == user.surname
        assert resp['status_code'] == '200'

    def test_get_inexistent_user_surname(self):
        user = self.builder.create_user()
        resp = client.get_user_surname(user.name)

        assert resp['body'] == f'Surname for user {user.name} not found'
        assert resp['status_code'] == '404'


class TestPutRequest(TestBase):
    def test_update_user_surname(self):
        user = self.builder.create_user()
        SURNAME_DATA[user.name] = user.surname

        resp = client.update_user_surname(user.name, user.new_surname)

        assert resp['status_code'] == '202'
        assert resp['body'] == user.new_surname

    def test_update_inexistent_user_surname(self):
        user = self.builder.create_user()

        resp = client.update_user_surname(user.name, user.new_surname)

        assert resp['status_code'] == '404'
        assert resp['body'] == f'Surname for user {user.name} not found'


class TestDeleteRequest(TestBase):
    def test_delete_user_surname(self):
        user = self.builder.create_user()
        SURNAME_DATA[user.name] = user.surname
        resp = client.delete_user_surname(user.name)

        assert resp['status_code'] == '204'
        assert resp['body'] == ''

    def test_delete_inexistent_user_surname(self):
        user = self.builder.create_user()
        resp = client.delete_user_surname(user.name)

        assert resp['status_code'] == '404'
        assert resp['body'] == f'Surname for user {user.name} not found'

