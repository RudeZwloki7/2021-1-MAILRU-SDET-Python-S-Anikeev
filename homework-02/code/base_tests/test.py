import allure
import pytest
from base_tests.base import BaseCase
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.UI
@allure.epic("SDET-Python-homework-2")
@allure.feature("UI tests")
class TestLogin(BaseCase):
    @allure.story("Login test")
    @allure.description("""
                            This test check correct authorization of user with
                            valid login and password.
                            After try of authorization it checks if redirection
                            in user account page is successful.
    """)
    def test_login(self):
        self.main_page.user_login()
        assert '/dashboard' in self.driver.current_url

    is_authorized = False

    @allure.story("Parametrized negative login test")
    @allure.description("""
                                This test check correct behavior authorization of user with
                                invalid login or password.
                                After try of authorization it checks if user is redirected 
                                ro page with error message of incorrect log in.
        """)
    @pytest.mark.parametrize(
        'email, password',
        [
            pytest.param(
                'wrong@mail.ru',
                '777qwerty'
            ),
            pytest.param(
                'invalidlogin',
                'asdf123'
            ),
        ]
    )
    def test_negative_login(self, email, password):
        self.main_page.user_login(email, password)
        if self.main_page.url != self.driver.current_url:
            assert 'Invalid login or password' == self.main_page.find(self.main_page.locators.ERROR_MSG_LOCATOR).text
        else:
            self.main_page.wait().until(EC.visibility_of_element_located(self.main_page.locators.ERROR_NOTIFICATION))
            notification = self.main_page.find(self.main_page.locators.ERROR_NOTIFICATION)
            assert 'Введите email или телефон' == notification.text


@pytest.mark.UI
@allure.epic("SDET-Python-homework-2")
@allure.feature("UI tests")
class TestCampaign(BaseCase):

    @allure.story("Test creation new campaign")
    @allure.description("""
                                This test automatically authorized in user account
                                with valid login and password and create new campaign.
                                After successful creation of new campaign it checks does
                                campaign in all campaign list on main page with the same 
                                name as name of just created campaign is shown.
        """)
    def test_create_campaign(self, logo_path):
        campaign_page = self.account_page.go_to_campaign()
        assert campaign_page.is_opened()
        is_created = campaign_page.create_campaign(logo_path)
        assert is_created


@pytest.mark.UI
@allure.epic("SDET-Python-homework-2")
@allure.feature("UI tests")
class TestSegment(BaseCase):

    @allure.story("Test creation new segment")
    @allure.description("""
                                    This test automatically authorized in user account
                                    with valid login and password and create new segment
                                    with given name.
                                    After successful creation of new segment it checks does
                                    segment with given name is shown in all created segments list.
            """)
    def test_create_segment(self, generate_name):
        segment_page = self.account_page.go_to_segment()
        assert segment_page.is_opened()
        created_segment = segment_page.create_segment(generate_name)
        assert generate_name == created_segment

    @allure.story("Test deletion segment")
    @allure.description("""
                                        This test automatically authorized in user account
                                        with valid login and password and delete segment
                                        with given name. If segment with given name occasionally
                                        doesn't exist it would create this segment and delete after
                                        that.
                                        After attempt of deletion the segment it checks if deletion
                                        was successful.
                """)
    def test_delete_segment(self, generate_name):
        segment_page = self.account_page.go_to_segment()
        assert segment_page.is_opened()
        is_deleted = segment_page.delete_segment(generate_name)
        assert is_deleted
