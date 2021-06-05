from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.register_page import RegisterPage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def login(self, username, password):
        self.insert(username, self.locators.USERNAME_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.click(self.locators.SUBMIT_BTN_LOCATOR)

    def go_to_registration_page(self):
        self.click(self.locators.REG_REF_LOCATOR)
        return RegisterPage(self.driver)
