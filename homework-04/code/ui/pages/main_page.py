from ui.locators.locators_android import MainPageANDROIDLocators
from ui.pages.base_page import BasePageANDROID, EC
from ui.pages.settings_page import SettingsPageANDROID


class MainPageANDROID(BasePageANDROID):
    locators = MainPageANDROIDLocators()

    def enter_value_in_search_field(self, text):
        self.find(self.locators.INPUT_FIELD).send_keys(text)
        self.driver.hide_keyboard()

    def interact_with_window(self):
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field('Russia')
        self.click_for_android(self.locators.SEND_QUERY)

        assert 'Россия' in self.find(self.locators.CARD_TITLE).text

        self.wait().until(EC.visibility_of_element_located(self.locators.SUGGESTS_LIST))
        self.swipe_left(self.locators.SUGGESTS_LIST, 3)
        self.click_for_android(self.locators.POPULATION_RUSSIA)
        self.wait().until(EC.text_to_be_present_in_element(self.locators.CARD_TITLE, '146'))

        return self.find(self.locators.CARD_TITLE).text

    def calc_exp(self, expression):
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field(expression)
        self.click_for_android(self.locators.SEND_QUERY)
        result = self.find(self.locators.RESPONSE).text

        return result

    def check_news_source_info(self):
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field('news')
        self.click_for_android(self.locators.SEND_QUERY)

        assert 'Вести ФМ' == self.find(self.locators.NEWS_PLAYER_TITLE).text

    def go_to_settings_page(self):
        self.click_for_android(self.locators.MENU_BTN)

        return SettingsPageANDROID(self.driver, self.config)
