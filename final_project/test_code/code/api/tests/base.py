import pytest
from orm.client import MysqlClient
from api.client.client import ApiClient
from utils.builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_client, logger):
        self.logger = logger
        self.builder: Builder = Builder()
        self.mysql_client: MysqlClient = mysql_client
        self.api_client: ApiClient = api_client
        if self.authorize:
            user = self.builder.create_user(username='test_user', email='mail@email.com', password='12345')
            if self.mysql_client.find_user(user.username) is None:
                self.logger.debug("test_user doesn't exist")
                self.mysql_client.add_user(user)

            assert self.mysql_client.find_user(user.username)
            self.api_client.post_login(user.username, user.password)
