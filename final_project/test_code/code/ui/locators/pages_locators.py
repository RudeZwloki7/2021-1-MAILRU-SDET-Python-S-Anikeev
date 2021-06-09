from selenium.webdriver.common.by import By


class BasePageLocators:
    NOTIFICATION_LOCATOR = (By.ID, 'flash')
    FOOTER_LOCATOR = (By.XPATH, '//p[contains(text(),"powered by")]')


class LoginPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.ID, 'username')
    PASSWORD_LOCATOR = (By.ID, 'password')
    SUBMIT_BTN_LOCATOR = (By.ID, 'submit')
    REG_REF_LOCATOR = (By.XPATH, '//a[@href="/reg"]')


class RegisterPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.ID, 'username')
    EMAIL_LOCATOR = (By.ID, 'email')
    PASSWORD_LOCATOR = (By.ID, 'password')
    CONFIRM_PASSWORD_LOCATOR = (By.ID, 'confirm')
    CHECKBOX_LOCATOR = (By.ID, 'term')
    SUBMIT_BTN_LOCATOR = (By.ID, 'submit')
    REG_CARD_LOCATOR = (By.ID, 'content')


class MainPageLocators(BasePageLocators):
    LOGOUT_BTN_LOCATOR = (By.ID, 'logout')
    PYTHON_LOCATOR = (By.LINK_TEXT, 'Python')
    PYTHON_HISTORY_LOCATOR = (By.LINK_TEXT, 'Python history')
    FLASK_LOCATOR = (By.LINK_TEXT, 'About Flask')
    LINUX_LOCATOR = (By.LINK_TEXT, 'Linux')
    CENTOS_LOCATOR = (By.LINK_TEXT, 'Download Centos7')
    NETWORK_LOCATOR = (By.LINK_TEXT, 'Network')
    NEWS_LOCATOR = (By.XPATH, '//a[text()="News"]')
    DOWNLOAD_LOCATOR = (By.XPATH, '//a[text()="Download"]')
    EXAMPLES_LOCATOR = (By.XPATH, '//a[contains(text(), "Examples")]')
    API_LOCATOR = (By.XPATH, '//div[contains(text(),"API")]/parent::div/figure')
    FUTURE_OF_INTERNET_LOCATOR = (By.XPATH, '//div[contains(text(),"Future")]/parent::div/figure')
    SMTP_LOCATOR = (By.XPATH, '//div[contains(text(),"SMTP")]/parent::div/figure')
    USERNAME_LOCATOR = (By.XPATH, '//div[@id="login-name"]/ul/li[1]')
    VK_ID_LOCATOR = (By.XPATH, '//div[@id="login-name"]/ul/li[2]')
    QUOTE_LOCATOR = (By.XPATH, '//footer/div/p[2]')
