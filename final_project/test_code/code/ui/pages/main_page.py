import allure

from ui.locators.pages_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    url = 'http://myapp:8090/welcome/'
    locators = MainPageLocators()

    @allure.step('Go to python page')
    def go_python_page(self):
        self.click(self.locators.PYTHON_LOCATOR)

    @allure.step('Go to python history page')
    def go_python_history_page(self):
        self.go_by_link_in_list(self.locators.PYTHON_LOCATOR, self.locators.PYTHON_HISTORY_LOCATOR)

    @allure.step('Go to flask page')
    def go_flask_page(self):
        self.go_by_link_in_list(self.locators.PYTHON_LOCATOR, self.locators.FLASK_LOCATOR)

    @allure.step('Go to linux page')
    def go_linux_page(self):
        self.click(self.locators.LINUX_LOCATOR)

    @allure.step('Go to centos page')
    def go_centos_page(self):
        self.go_by_link_in_list(self.locators.LINUX_LOCATOR, self.locators.CENTOS_LOCATOR)

    @allure.step('Go to network page')
    def go_network_page(self):
        self.click(self.locators.NETWORK_LOCATOR)

    @allure.step('Go to news page')
    def go_news_page(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.NEWS_LOCATOR)

    @allure.step('Go to download page')
    def go_download_page(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.DOWNLOAD_LOCATOR)

    @allure.step('Go to examples page')
    def go_examples(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.EXAMPLES_LOCATOR)

    @allure.step('Go to api page')
    def go_api(self):
        self.click(self.locators.API_LOCATOR)

    @allure.step('Go to future of internet page')
    def go_future_of_internet(self):
        self.click(self.locators.FUTURE_OF_INTERNET_LOCATOR)

    @allure.step('Go to SMTP page')
    def go_smtp(self):
        self.click(self.locators.SMTP_LOCATOR)

    @allure.step('Log out')
    def logout(self):
        self.click(self.locators.LOGOUT_BTN_LOCATOR)

    def go_by_link_in_list(self, list_locator, link_locator):
        self.action_chains.move_to_element(self.find(list_locator)).perform()
        self.action_chains.move_to_element(self.find(link_locator)).click().perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])
