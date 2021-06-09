import pytest
from orm.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='test_db')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()
