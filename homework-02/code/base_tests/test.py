import os
import allure
import pytest
from base_tests.base import BaseCase


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
                'another@mail.ru',
                'asdf123'
            ),
        ]
    )
    def test_negative_login(self, email, password):
        self.main_page.user_login(email, password)
        assert "Error. Try again later." in self.driver.page_source


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
        campaign_name = campaign_page.create_campaign(logo_path)
        created_campaign = (self.account_page.locators.CREATED_CAMPAIGN[0],
                            self.account_page.locators.CREATED_CAMPAIGN[1].format(campaign_name))
        assert campaign_name == campaign_page.find(created_campaign).text

    @pytest.fixture(scope='function')
    def logo_path(self, repo_root):
        return os.path.join(repo_root, 'ui', 'logo.png')


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
    def test_create_segment(self, name):
        segment_page = self.account_page.go_to_segment()
        assert segment_page.is_opened()
        created_segment = segment_page.create_segment(name)
        assert name == created_segment

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
    def test_delete_segment(self, name):
        segment_page = self.account_page.go_to_segment()
        assert segment_page.is_opened()
        is_deleted = segment_page.delete_segment(name)
        assert is_deleted

    @pytest.fixture(scope="class")
    def name(self):
        import random
        return f"default{random.randint(0, 100)}"

