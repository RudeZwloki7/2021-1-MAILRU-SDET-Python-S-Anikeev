from ui.pages.base_page import BasePage
from ui.locators.locators_web import MainPageLocators
from ui.locators.locators_mw import MainPagePageMWLocators
from ui.locators.locators_android import MainPageANDROIDLocators
import allure


class MainPage(BasePage):
    locators = MainPageLocators()

    def interact_with_window(self):
        pass

    def enter_value_in_search_field(self, text):
        pass

    def calc_exp(self, expression):
        pass

    def select_news_fm_source(self):
        pass


class MainPageMW(MainPage):
    locators = MainPagePageMWLocators()

    @allure.step("Нажимаем на кнопку поиска")
    def click_on_search_button(self):
        self.click(self.locators.SEARCH_ICON)

    @allure.step("Нажимаем на кнопку открытия меню (mobile)")
    def open_menu_button(self):
        self.click(self.locators.MAIN_MENU)

    @allure.step("Нажимаем на кнопку открытия меню (mobile)")
    def open_watchlist(self):
        self.click(self.locators.WATCH_LIST)


class MainPageANDROID(BasePage):
    locators = MainPageANDROIDLocators()

    def enter_value_in_search_field(self, text):
        self.find(self.locators.INPUT_FIELD).send_keys(text)
        self.driver.hide_keyboard()

    def interact_with_window(self):
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field('Russia')
        self.click_for_android(self.locators.SEND_QUERY)
        # self.main_page.swipe_element_lo_left(self.main_page.locators.SUGGESTS_LIST)
        # self.scroll_left(self.locators.SUGGESTS_LIST)
        self.click_for_android(self.locators.POPULATION_RUSSIA)
        return self.find(self.locators.CARD_TITLE).text

    def calc_exp(self, expression):
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field(expression)
        self.click_for_android(self.locators.SEND_QUERY)
        result = self.find(self.locators.RESPONSE).text

        return result

    def select_news_fm_source(self):
        self.click_for_android(self.locators.MENU_BTN)
        self.swipe_to_element(self.locators.NEWS_SOURCE, 3)
        self.click_for_android(self.locators.NEWS_SOURCE)
        self.click_for_android(self.locators.NEWS_FM)
        y_coord = self.find(self.locators.NEWS_FM).location['y']
        check_y_coord = self.find(self.locators.NEWS_CHECK).location['y']
        assert y_coord == check_y_coord

        self.driver.back()
        self.driver.back()
        self.click_for_android(self.locators.SEARCH_KEYBOARD)
        self.enter_value_in_search_field('news')
        self.click_for_android(self.locators.SEND_QUERY)
        assert 'Вести ФМ' == self.find(self.locators.NEWS_PLAYER_TITLE).text
