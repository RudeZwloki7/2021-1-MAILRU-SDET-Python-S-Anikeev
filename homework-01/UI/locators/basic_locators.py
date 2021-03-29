from selenium.webdriver.common.by import By

LOGIN_LOCATOR = (By.XPATH, '//*[contains(@class,"responseHead-module-button") and contains(text(), "Войти")]')
EMAIL_LOCATOR = (By.NAME, 'email')
PASSWORD_LOCATOR = (By.NAME, 'password')
SUBMIT_LOGIN_LOCATOR = (By.XPATH, '//*[contains(text(), "Войти") and contains(@ class, "authForm-module-button")]')

USER_LOCATOR = (By.XPATH, '//*[contains(@ class, "right-module-rightButton")]')
LOGOUT_LOCATOR = (By.XPATH, '//*/a[contains(@ class, "rightMenu-module") and contains(@ href, "/logout" )]')

PROFILE_LOCATOR = (By.XPATH, '//*[contains(@ class, "center-module") and contains(@ href, "/profile" )]')
PROFILE_FULLNAME_LOCATOR = (By.XPATH, '//div[contains(@ data-name, "fio")]//input')
PROFILE_PHONE_LOCATOR = (By.XPATH, '//div[contains(@ data-name, "phone")]//input')
PROFILE_EMAIL_LOCATOR = (By.XPATH, '//div[contains(@ class, "js-additional-email profile")]//input')
PROFILE_NOTIFICATION_LOCATOR = (By.XPATH, '//div[contains(@ cid, "view") and contains(@ class, "_notification")]')
SAVE_PROFILE_LOCATOR = (By.XPATH, '//div[@class = "button__text" and contains(text(), "Сохранить")]')
