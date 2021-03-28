import time
import pytest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from UI.locators import basic_locators

CLICK_RETRY = 3


class User:
    driver = None
    config = None
    email = 'javatest715@gmail.com'
    password = 'sh@ndi7'

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config

    def user_logout(self):
        self.click(basic_locators.USER_LOCATOR)
        # Wait for ul transition
        time.sleep(0.4)
        self.click(basic_locators.LOGOUT_LOCATOR)
        self.find(basic_locators.LOGIN_LOCATOR)

    def user_edit_profile(self):
        self.click(basic_locators.PROFILE_LOCATOR)
        fields = self.find_all(basic_locators.PROFILE_FORMS_LOCATOR)
        input_text = ['Иванов Арнольд Петрович', '+7945321789', 'mymail@mail.ru']
        for i in range(len(fields)):
            fields[i].clear()
            fields[i].send_keys(input_text[i])
        self.click(basic_locators.SAVE_PROFILE_LOCATOR)

    def user_navigate(self, btn_name):
        self.wait().until(EC.presence_of_element_located(basic_locators.PROFILE_LOCATOR))
        self.click((By.XPATH, '//ul[contains(@ class,"center-module-buttonsWrap")]/li/a[contains(text(), "'
                    + btn_name + '")]'))
        self.wait().until(EC.url_changes)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_all(self, locator, timeout=None):
        return self.wait(timeout).until((EC.presence_of_all_elements_located(locator)))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def insert(self, text, locator):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    @pytest.fixture(scope='function')
    def login(self, setup):
        # self.find(basic_locators.LOGIN_LOCATOR).click()
        self.click(basic_locators.LOGIN_LOCATOR)
        User.insert(self, self.email, basic_locators.EMAIL_LOCATOR)
        User.insert(self, self.password, basic_locators.PASSWORD_LOCATOR)
        self.click(basic_locators.SUBMIT_LOGIN_LOCATOR)
        self.wait().until(EC.invisibility_of_element_located(
            (By.XPATH, '//*[contains(@ class,"spinner-module-large")')))

    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
