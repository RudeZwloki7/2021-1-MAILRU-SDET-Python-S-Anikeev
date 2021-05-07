import pytest
import os

from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_table('all_requests')
        mysql_client.create_table('requests_by_type')
        mysql_client.create_table('most_frequent_requests')
        mysql_client.create_table('client_err_requests')
        mysql_client.create_table('server_err_requests')

        mysql_client.connection.close()


def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))
