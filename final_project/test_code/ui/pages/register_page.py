from ui.locators.pages_locators import RegisterPageLocators
from ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    url = 'http://0.0.0.0:8080/reg'
    locators = RegisterPageLocators()

    def register_user(self, username, email, password, confirm_password):
        self.insert(username, self.locators.USERNAME_LOCATOR)
        self.insert(email, self.locators.EMAIL_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.insert(confirm_password, self.locators.CONFIRM_PASSWORD_LOCATOR)
        self.click(self.locators.CHECKBOX_LOCATOR)
        self.click(self.locators.SUBMIT_BTN_LOCATOR)
