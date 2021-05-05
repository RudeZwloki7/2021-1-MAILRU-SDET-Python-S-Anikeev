from appium.webdriver.common.mobileby import MobileBy


class BasePageANDROIDLocators:
    pass


class MainPageANDROIDLocators(BasePageANDROIDLocators):
    SEARCH_KEYBOARD = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    INPUT_FIELD = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    SEND_QUERY = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_action')
    SUGGESTS_LIST = (MobileBy.ID, 'ru.mail.search.electroscope:id/suggests_list')
    POPULATION_RUSSIA = (MobileBy.XPATH, '//android.widget.TextView[@text = "численность населения россии"]')
    CARD_TITLE = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    RESPONSE = (MobileBy.XPATH, '//android.widget.TextView[@index="2"]')
    MENU_BTN = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    NEWS_PLAYER_TITLE = (MobileBy.ID, 'ru.mail.search.electroscope:id/player_track_name')


class SettingsPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCE = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')


class NewsSourcePageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_FM = (MobileBy.XPATH, ' //android.widget.TextView[@text = "Вести FM"]')
    NEWS_CHECK = (MobileBy.ID, 'ru.mail.search.electroscope:id/news_sources_item_selected')
