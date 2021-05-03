import allure
from selenium.common.exceptions import TimeoutException
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import AccountPageLocators
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentPage


class AccountPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = AccountPageLocators()

    @allure.step('Go to campaign page')
    def go_to_campaign(self):
        try:
            create_locator = self.locators.CREATE_CAMPAIGN
            self.find(create_locator)
        except TimeoutException:
            create_locator = self.locators.CREATE_ANOTHER_CAMPAIGN

        self.click(create_locator)
        return CampaignPage(self.driver)

    @allure.step('Go to segment page')
    def go_to_segment(self):
        self.click(self.locators.SEGMENT_PAGE_LOCATOR)
        return SegmentPage(self.driver)
