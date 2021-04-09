import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import CampaignPageLocators


class CampaignPage(BasePage):
    url = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators()

    @allure.step("Creation new campaign")
    def create_campaign(self, logo_path, url='https://github.com/RudeZwloki7', target='_traffic'):
        target_locator = (self.locators.CAMPAIGN_TARGET_TEMPLATE[0],
                          self.locators.CAMPAIGN_TARGET_TEMPLATE[1].format(target))
        self.click(target_locator)
        self.insert(url, self.locators.INSERT_URL)
        campaign_name = self.find(self.locators.CAMPAIGN_NAME)
        self.scroll_to(campaign_name)
        campaign_name = campaign_name.get_attribute('value')
        self.scroll_to(self.find(self.locators.AD_FORMAT_BANNER))
        self.click(self.locators.AD_FORMAT_BANNER)
        self.scroll_to(self.find(self.locators.UPLOAD_IMAGE_BUTTON))
        self.find(self.locators.UPLOAD_IMAGE_BUTTON).send_keys(logo_path)
        self.click(self.locators.SUBMIT_LOCATOR)

        return campaign_name
