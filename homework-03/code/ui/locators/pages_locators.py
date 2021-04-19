from selenium.webdriver.common.by import By


class BasePageLocators:
    BASE_PAGE_LOADED_LOCATOR = (By.XPATH, '//div[contains(@class, "mainPage-module-promo")]')
    LOGIN_BUTTON = (By.XPATH, '//*[contains(@class,"responseHead-module-button") and contains(text(), "Войти")]')


class MainPageLocators(BasePageLocators):
    EMAIL_LOCATOR = (By.NAME, 'email')
    PASSWORD_LOCATOR = (By.NAME, 'password')
    SUBMIT_LOCATOR = (By.XPATH, '//*[contains(text(), "Войти") and contains(@ class, "authForm-module-button")]')
    ERROR_MSG_LOCATOR = (By.XPATH, '//div[contains(@class, "formMsg_text")]')
    ERROR_NOTIFICATION = (By.XPATH, '//div[contains(@class, "notify-module-error")]')


class AccountPageLocators(BasePageLocators):
    CREATE_CAMPAIGN = (By.XPATH, '//a[@href="/campaign/new"]')
    CREATE_ANOTHER_CAMPAIGN = \
        (By.XPATH, '//div[contains(@class , "button-module-textWrapper") and contains(text(), "Создать кампанию")]')
    INSTRUCTION_LOCATOR = (By.XPATH,
                           '//div[contains(@class,"instruction-module") and contains(text(), "С чего начать")]')
    CREATED_CAMPAIGN = (By.XPATH, '//a[contains(@class, "nameCell-module-campaignName") and @title="{}"]')
    SEGMENT_PAGE_LOCATOR = (By.XPATH, '//a[@href ="/segments"]')
    SPINNER_LOCATOR = (By.XPATH, '//*[contains(@ class,"spinner-module-large")')


class CampaignPageLocators(AccountPageLocators):
    CAMPAIGN_TARGET_TEMPLATE = (By.XPATH, '//div[contains(@class, "column-list-item {}")]')
    INSERT_URL = (By.XPATH, '//input[@data-gtm-id="ad_url_text"]')
    CAMPAIGN_NAME = (By.XPATH, '//div[contains(@class, "base-settings__campaign-name-wrap")]//input')
    AD_FORMAT_BANNER = (By.XPATH, '//span[contains(text(), "Баннер")]')
    UPLOAD_IMAGE_BUTTON = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]/'
                                     'div[contains(@class, "upload-module-wrapper")]//input')
    SUBMIT_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]/div[contains(text(), "Создать кампанию")]')


class SegmentPageLocators(AccountPageLocators):
    CREATE_SEGMENT = (By.XPATH, '//a[@href ="/segments/segments_list/new/"]')
    COUNT_SEGMENTS = (By.XPATH, '//a[@href="/segments/segments_list"]/span[contains(@class, "item-count")]')
    SEGMENT_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@class, "adding-segments-source")]')
    ADD_SEGMENT = (By.XPATH, '//div[@class="button__text" and contains(text(), "Добавить сегмент")]')
    SEGMENT_NAME = (By.XPATH, '//input[@maxlength="60" and contains(@class,"input__inp")]')
    CREATE_NEW_SEGMENT = (By.XPATH, '//button[@data-class-name="Submit"]')
    SEGMENT_LIST_TEMPLATE = (By.XPATH, '//a[contains(@href, "/segments/segments_list/") and @title="{}"]')
    DELETE_SEGMENT_TEMPLATE = (By.XPATH, '//div[contains(@data-test, "remove") and @data-row-id="{}"]')
    SUBMIT_DELETION = (By.XPATH, '//div[@class = "button__text" and contains(text(), "Удалить")]')
