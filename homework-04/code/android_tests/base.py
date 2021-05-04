import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePageANDROID
from ui.pages.main_page import MainPageANDROID


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePageANDROID = request.getfixturevalue('base_page')
        self.main_page: MainPageANDROID = request.getfixturevalue('main_page')

        self.logger.debug('Initial setup done!')
