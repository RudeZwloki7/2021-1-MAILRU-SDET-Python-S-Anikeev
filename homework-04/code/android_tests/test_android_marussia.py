import pytest
from android_tests.base import BaseCase


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
        settings_page = self.main_page.go_to_settings_page()
        news_source_page = settings_page.go_to_news_source_page()
        news_source_page.choose_news_source()
        news_source_page.return_to_main_page()
        self.main_page.check_news_source_info()
