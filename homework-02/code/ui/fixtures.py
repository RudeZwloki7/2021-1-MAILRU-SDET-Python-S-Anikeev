import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ui.pages.account_page import AccountPage
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


def get_driver(browser_name, download_dir):
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})

        manager = ChromeDriverManager(version='latest')
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest', log_level=0)  # set log_level=0 to disable logging
        browser = webdriver.Firefox(executable_path=manager.install())
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')

    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']

    browser = get_driver(browser_name, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    url = config['url']

    browser = get_driver(request.param, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope="function")
@allure.step("Log in")
def autologin(driver, main_page, logger, email='wqew.asdas@mail.ru', password='tester404'):
    main_page.click(main_page.locators.LOGIN_BUTTON)
    main_page.insert(email, main_page.locators.EMAIL_LOCATOR)
    main_page.insert(password, main_page.locators.PASSWORD_LOCATOR)
    main_page.click(main_page.locators.SUBMIT_LOCATOR)
    logger.info(f'Logged in with email: {email} and password: {password}')

    return AccountPage(driver)


@pytest.fixture(scope='function')
def logo_path(repo_root):
    return os.path.join(repo_root, 'ui', 'logo.png')


@pytest.fixture(scope="class")
def generate_name():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))
