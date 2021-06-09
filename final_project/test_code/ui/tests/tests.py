import pytest
from ui.tests.base import BaseCase
from utils.str_values import MainPageUrls


@pytest.mark.UI
@pytest.mark.skip
class TestLogin(BaseCase):
    is_authorized = False

    def test_login(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(username=user.username)

        main_page = self.login_page.login(user.username, user.password)

        assert main_page.is_visible(main_page.locators.FOOTER_LOCATOR)
        assert self.driver.current_url == main_page.url
        assert user.vk_id in main_page.find(main_page.locators.VK_ID_LOCATOR).text

        self.mysql_client.delete_user(user.username)

    def test_incorrect_username_length_login(self):
        main_page = self.login_page.login(self.builder.random_letter(), self.builder.random_letter())

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    def test_invalid_login(self):
        user = self.builder.create_user()
        main_page = self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Invalid username or password'

    def test_blank_pass_login(self):
        user = self.builder.create_user(password=' ')
        main_page = self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Необходимо указать пароль для авторизации'

    def test_invalid_login_and_passwd(self):
        user = self.builder.create_user(username=self.builder.random_letter(), password=' ')
        main_page = self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    def test_blocked_user_login(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user=user, access=0)
        assert self.mysql_client.find_user(username=user.username)

        main_page = self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Ваша учетная запись заблокирована'

        self.mysql_client.delete_user(user.username)


@pytest.mark.UI
@pytest.mark.skip
class TestRegistration(BaseCase):
    is_authorized = False

    def test_register(self):
        user = self.builder.create_user()
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username)
        assert self.driver.current_url == main_page.url

        self.mysql_client.delete_user(user.username)

    def test_incorrect_username_length(self):
        user = self.builder.create_user(username=self.builder.random_letter())
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    def test_incorrect_email_length(self):
        user = self.builder.create_user(email=self.builder.random_letter())
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect email length'

    def test_incorrect_username_and_email(self):
        user = self.builder.create_user(username=self.builder.random_letter(),
                                        email=self.builder.random_letter())

        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    def test_blank_pass_reg(self):
        user = self.builder.create_user(password=' ')
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(
            reg_page.locators.NOTIFICATION_LOCATOR).text == 'Необходимо указать пароль для регистрации'

    def test_invalid_email(self):
        user = self.builder.create_user(email=self.builder.random_string())
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Invalid email address'

    def test_unmatch_pass(self):
        user = self.builder.create_user(password_repeat=self.builder.random_digit())
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Passwords must match'

    @pytest.mark.parametrize(
        'username, email',
        [
            pytest.param(
                'test_qa',
                'qa_test@mail.com'
            ),
            pytest.param(
                'test_qa2',
                'qa_test@mail.com'
            ),
            pytest.param(
                'test_qa',
                'qa_test2@mail.com'
            ),
        ]
    )
    def test_reg_exist_user(self, username, email):
        self.mysql_client.delete_user(username='test_qa',
                                      email='qa_test@mail.com')

        user = self.builder.create_user(username='test_qa',
                                        email='qa_test@mail.com')

        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(username=user.username)

        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(username, email, user.password, user.password_repeat)

        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'User already exist'

        self.mysql_client.delete_user(user.username)


@pytest.mark.UI
# @pytest.mark.skip
class TestMainPage(BaseCase):
    urls = MainPageUrls()

    def prepare(self):
        username = 'test_user'
        response = self.api_client.get_vk_id(username)
        import time
        time.sleep(10)
        assert username in self.main_page.find(self.main_page.locators.USERNAME_LOCATOR).text
        if response.status_code != 404:
            assert response.json()['vk_id'] in self.main_page.find(self.main_page.locators.VK_ID_LOCATOR).text
        quote = self.main_page.find(self.main_page.locators.QUOTE_LOCATOR).text
        assert quote != ''
        # assert quote in self.get_zen()

    def test_python(self):
        self.main_page.go_python_page()

        assert self.driver.current_url == self.urls.PYTHON_URL

    def test_python_history(self):
        self.main_page.go_python_history_page()

        assert self.driver.current_url == self.urls.PY_HISTORY_URL

    def test_flask(self):
        self.main_page.go_flask_page()
        assert self.driver.current_url == self.urls.FLASK_URL

    def test_linux(self):
        self.main_page.go_linux_page()

        assert self.driver.current_url == self.urls.LINUX_URL

    def test_centos(self):
        self.main_page.go_centos_page()

        assert self.driver.current_url == self.urls.CENTOS_URL

    def test_network(self):
        self.main_page.go_network_page()

        assert self.driver.current_url == self.urls.NETWORK_URL

    def test_news(self):
        self.main_page.go_news_page()

        assert self.driver.current_url == self.urls.WIRESHARK_NEWS_URL

    def test_downloads(self):
        self.main_page.go_download_page()

        assert self.driver.current_url == self.urls.WIRESHARK_DOWNLOAD_URL

    def test_examples(self):
        self.main_page.go_examples()

        assert self.driver.current_url == self.urls.TCPDUMP_EXAMPLES_URL

    def test_api(self):
        self.main_page.go_api()

        assert self.driver.current_url == self.urls.API_URL

    def test_future_of_internet(self):
        self.main_page.go_future_of_internet()

        assert self.driver.current_url == self.urls.FUTURE_OF_INTERNET_URL

    def test_smtp(self):
        self.main_page.go_smtp()

        assert self.driver.current_url == self.urls.SMTP_URL

    def test_logout(self):
        self.main_page.logout()
        user = self.mysql_client.find_user('test_user')

        assert user.active == 0
        assert self.driver.current_url == self.login_page.url
