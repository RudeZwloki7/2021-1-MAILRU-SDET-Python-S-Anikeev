import pytest

from mysql.builder import MySQLBuilder
from mysql.models import *


class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.prepare()


class TestMysql(MySQLBase):
    def test_all_requests(self):
        self.mysql_builder.create_all_requests()
        rows = self.mysql.session.query(AllRequests).all()
        print(rows)

        assert len(rows) == 1

    def test_requests_by_type(self):
        requests_list = self.mysql_builder.create_requests_by_type()
        rows = self.mysql.session.query(RequestsByType).all()
        print(rows)

        assert len(rows) == len(requests_list)

    def test_most_frequent_requests(self):
        requests_list = self.mysql_builder.create_most_frequent_requests()
        rows = self.mysql.session.query(MostFrequentRequests).all()
        print(rows)

        assert len(rows) == len(requests_list)

    def test_client_err_requests(self):
        requests_list = self.mysql_builder.create_client_err_requests()
        rows = self.mysql.session.query(ClientErrRequests).all()
        print(rows)

        assert len(rows) == len(requests_list)

    def test_server_err_requests(self):
        requests_list = self.mysql_builder.create_server_err_requests()
        rows = self.mysql.session.query(ServerErrRequests).all()
        print(rows)

        assert len(rows) == len(requests_list)
