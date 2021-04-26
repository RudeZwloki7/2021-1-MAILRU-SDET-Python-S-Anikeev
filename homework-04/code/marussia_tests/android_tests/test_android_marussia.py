import time
import allure
import pytest
from marussia_tests.base import BaseCase


class TestMarussiaAndroid(BaseCase):

    @pytest.mark.AndroidUI
    def test_interacting_with_window(self):
        result = self.main_page.interact_with_window()
        assert '146 млн.' in result

    @pytest.mark.AndroidUI
    def test_calculator(self):
        result = self.main_page.calc_exp('2*5')
        assert '10' == result

    @pytest.mark.AndroidUI
    def test_news_source(self):
        self.main_page.select_news_fm_source()
