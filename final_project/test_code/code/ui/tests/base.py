import pytest
from _pytest.fixtures import FixtureRequest
from api.client.vk_api_client import VkApiClient
from orm.client import MysqlClient
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from utils.builder import Builder


class BaseCase:
    is_authorized = True

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, mysql_client):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.builder = Builder()
        self.mysql_client: MysqlClient = mysql_client
        self.api_client: VkApiClient = VkApiClient()

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.is_authorized:
            user = self.builder.create_user(username='test_user', email='mail@email.com', password='12345')
            if self.mysql_client.find_user(user.username) is None:
                self.logger.debug("test_user doesn't exist")
                self.mysql_client.add_user(user)

            assert self.mysql_client.find_user(user.username)
            self.main_page: MainPage = request.getfixturevalue('autologin')
            self.logger.info('Set up authorized user page')

        self.prepare()
        self.logger.info('Initial setup done!')
