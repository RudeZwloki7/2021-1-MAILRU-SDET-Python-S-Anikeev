import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.account_page import AccountPage
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class BaseCase:
    is_authorized = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

        if self.is_authorized:
            self.account_page: AccountPage = request.getfixturevalue('autologin')
            self.logger.debug('Set up authorized user page')

        self.logger.debug('Initial setup done!')
