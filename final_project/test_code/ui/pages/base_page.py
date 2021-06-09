import logging

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators.pages_locators import BasePageLocators
from selenium.webdriver.support import expected_conditions as EC

CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class BasePage:
    url = 'http://myapp:8090'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def is_visible(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def insert(self, query, locator):
        field = self.find(locator)
        field.clear()
        field.send_keys(query)
        logger.info(f'Inserted "{query}" in {locator}')

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i + 1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
