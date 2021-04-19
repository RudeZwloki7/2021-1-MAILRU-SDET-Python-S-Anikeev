import allure
from ui.pages.base_page import BasePage, logger
from ui.locators.pages_locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step("Try to log in")
    def user_login(self, email='javatest715@gmail.com', password='sh@ndi7'):
        logger.info(f'Try to log in with {email} and {password}')
        self.click(self.locators.LOGIN_BUTTON)
        self.insert(email, self.locators.EMAIL_LOCATOR)
        self.insert(password, self.locators.PASSWORD_LOCATOR)
        self.click(self.locators.SUBMIT_LOCATOR)
        if '/dashboard' not in self.driver.current_url:
            return self.get_err_msg()

    def get_err_msg(self):
        if self.url != self.driver.current_url:
            return self.find(self.locators.ERROR_MSG_LOCATOR).text
        else:
            self.wait().until(EC.visibility_of_element_located(self.locators.ERROR_NOTIFICATION))
            return self.find(self.locators.ERROR_NOTIFICATION).text
