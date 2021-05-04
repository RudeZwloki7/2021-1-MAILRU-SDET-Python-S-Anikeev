from ui.locators.locators_android import SettingsPageANDROIDLocators
from ui.pages import BasePageANDROID
from ui.pages.news_source_page import NewsSourcePageANDROID


class SettingsPageANDROID(BasePageANDROID):
    locators = SettingsPageANDROIDLocators()

    def go_to_news_source_page(self):
        self.swipe_to_element(self.locators.NEWS_SOURCE, 3)
        self.click_for_android(self.locators.NEWS_SOURCE)
        return NewsSourcePageANDROID(self.driver, self.config)
