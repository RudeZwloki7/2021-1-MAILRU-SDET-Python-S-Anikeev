import logging

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from ui.locators.locators_android import BasePageANDROIDLocators


CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class BasePageANDROID(object):
    locators = BasePageANDROIDLocators()

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

        logger.info(f'{self.__class__.__name__} page is opening...')

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_all(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_all_elements_located(locator))

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i + 1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    @allure.step('Clicking {locator}')
    def click_for_android(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i + 1} of {CLICK_RETRY}...')
            try:
                self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def swipe_up(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, немного ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element(self, locator, max_swipes):
        """
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать вверх
        """
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def swipe_element_lo_left(self, locator):
        """
        Свайп элемента влево от центра элемента к его левому краю.

        :param locator: локатор, который мы ищем
        """
        web_element = self.find(locator, 10)
        left_x = web_element.location['x']
        middle_x = left_x + web_element.rect['width']/2
        upper_y = web_element.location['y']
        lower_y = upper_y + web_element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        action = TouchAction(self.driver)
        action. \
            press(x=middle_x, y=middle_y). \
            wait(ms=300). \
            move_to(x=left_x, y=middle_y). \
            release(). \
            perform()

    def swipe_left(self, locator, max_swipes):
        """
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать влево
        """

        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_element_lo_left(locator)
            already_swiped += 1

    def return_to_page(self, back_count):
        for i in range(back_count):
            self.driver.back()