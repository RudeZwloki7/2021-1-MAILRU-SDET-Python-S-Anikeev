from ui.locators.pages_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    url = 'http://0.0.0.0:8080/welcome/'
    locators = MainPageLocators()

    def go_python_page(self):
        self.click(self.locators.PYTHON_LOCATOR)

    def go_python_history_page(self):
        self.go_by_link_in_list(self.locators.PYTHON_LOCATOR, self.locators.PYTHON_HISTORY_LOCATOR)

    def go_flask_page(self):
        self.go_by_link_in_list(self.locators.PYTHON_LOCATOR, self.locators.FLASK_LOCATOR)

    def go_linux_page(self):
        self.click(self.locators.LINUX_LOCATOR)

    def go_centos_page(self):
        self.go_by_link_in_list(self.locators.LINUX_LOCATOR, self.locators.CENTOS_LOCATOR)

    def go_network_page(self):
        self.click(self.locators.NETWORK_LOCATOR)

    def go_news_page(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.NEWS_LOCATOR)

    def go_download_page(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.DOWNLOAD_LOCATOR)

    def go_examples(self):
        self.go_by_link_in_list(self.locators.NETWORK_LOCATOR, self.locators.EXAMPLES_LOCATOR)

    def go_api(self):
        self.click(self.locators.API_LOCATOR)

    def go_future_of_internet(self):
        self.click(self.locators.FUTURE_OF_INTERNET_LOCATOR)

    def go_smtp(self):
        self.click(self.locators.SMTP_LOCATOR)

    def logout(self):
        self.click(self.locators.LOGOUT_BTN_LOCATOR)

    def go_by_link_in_list(self, list_locator, link_locator):
        self.action_chains.move_to_element(self.find(list_locator)).perform()
        self.action_chains.move_to_element(self.find(link_locator)).click().perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])
