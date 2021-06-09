import allure

from ui.locators.pages_locators import RegisterPageLocators
from ui.pages.base_page import BasePage, logger
from ui.pages.main_page import MainPage


class RegisterPage(BasePage):
    url = 'http://myapp:8090/reg'
    locators = RegisterPageLocators()

    @allure.step('Register new user')
    def register_user(self, username, email, password, confirm_password):
        logger.info(f'Try to register')
        self.is_visible(self.locators.REG_CARD_LOCATOR)
        self.insert(username, self.locators.USERNAME_LOCATOR)
        self.insert(email, self.locators.EMAIL_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.insert(confirm_password, self.locators.CONFIRM_PASSWORD_LOCATOR)
        self.click(self.locators.CHECKBOX_LOCATOR)
        self.click(self.locators.SUBMIT_BTN_LOCATOR)

        return MainPage(self.driver)
