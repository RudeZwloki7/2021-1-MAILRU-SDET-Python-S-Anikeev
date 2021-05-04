from ui.locators.locators_android import NewsSourcePageANDROIDLocators
from ui.pages import BasePageANDROID


class NewsSourcePageANDROID(BasePageANDROID):
    locators = NewsSourcePageANDROIDLocators()

    def choose_news_source(self):
        self.click_for_android(self.locators.NEWS_FM)
        y_coord = self.find(self.locators.NEWS_FM).location['y']
        check_y_coord = self.find(self.locators.NEWS_CHECK).location['y']
        assert y_coord == check_y_coord

    def return_to_main_page(self):
        self.return_to_page(2)
