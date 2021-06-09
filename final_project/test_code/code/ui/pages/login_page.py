import allure

from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage, logger
from ui.pages.register_page import RegisterPage

from ui.pages.main_page import MainPage


class LoginPage(BasePage):
    url = 'http://myapp:8090/login'
    locators = LoginPageLocators()

    @allure.step('Log in with')
    def login(self, username, password):
        logger.info(f'Try to log in')
        self.insert(username, self.locators.USERNAME_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.click(self.locators.SUBMIT_BTN_LOCATOR)
        return MainPage(self.driver)

    @allure.step('Go to registration page')
    def go_to_registration_page(self):
        self.click(self.locators.REG_REF_LOCATOR)
        return RegisterPage(self.driver)
