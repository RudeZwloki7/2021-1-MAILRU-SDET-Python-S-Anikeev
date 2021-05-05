import os
import allure
import pytest
from appium import webdriver
from ui.capability import get_capability
from ui.pages import MainPageANDROID
from ui.pages.base_page import BasePageANDROID


@pytest.fixture
def base_page(driver, config):
    return BasePageANDROID(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    return MainPageANDROID(driver=driver, config=config)


def get_driver(appium_url):
    desired_caps = get_capability()
    driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
    return driver


@pytest.fixture(scope='function')
def driver(config, test_dir):
    appium_url = config['appium']
    browser = get_driver(appium_url)
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)
