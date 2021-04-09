import allure
from ui.pages.base_page import BasePage, logger
from ui.locators.pages_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step("Try to log in")
    def user_login(self, email='javatest715@gmail.com', password='sh@ndi7'):
        logger.info(f'Try to log in with {email} and {password}')
        self.click(self.locators.LOGIN_BUTTON)
        self.insert(email, self.locators.EMAIL_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.click(self.locators.SUBMIT_LOCATOR)

