import pytest
from ui.tests.base import BaseCase


# TODO: write tests with checking username and vk_id
@pytest.mark.UI
class TestLogin(BaseCase):
    is_authorized = False

    def test_login(self, username='test_user', password='12345'):
        self.login_page.login(username, password)
        assert self.driver.current_url == self.login_page.url + '/welcome/'


class TestRegistration(BaseCase):

    def test_register(self, username='qwerty', email='dasd@mail.com', password='asdasa', confirm_password='asdasa'):
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(username, email, password, confirm_password)

        assert self.driver.current_url == self.login_page.url + '/welcome/'


class TestMainPage(BaseCase):
    python_url = 'https://www.python.org/'
    py_history_url = 'https://en.wikipedia.org/wiki/History_of_Python'
    flask_url = 'https://flask.palletsprojects.com/en/1.1.x/#'
    linux_url = 'https://www.linux.org/'
    centos_url = 'https://www.centos.org/download/'
    network_url = 'https://en.wikipedia.org/wiki/Telecommunications_network'
    wireshark_news_url = 'https://www.wireshark.org/news/'
    wireshark_download_url = 'https://www.wireshark.org/#download'
    tcpdump_examples_url = 'https://hackertarget.com/tcpdump-examples/'
    api_url = 'https://en.wikipedia.org/wiki/API'
    future_of_internet_url ='https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'
    smtp_url = 'https://ru.wikipedia.org/wiki/SMTP'

    def test_python(self):
        self.main_page.go_python_page()

        assert self.driver.current_url == self.python_url

    def test_python_history(self):
        self.main_page.go_python_history_page()

        assert self.driver.current_url == self.py_history_url

    def test_flask(self):
        self.main_page.go_flask_page()
        assert self.driver.current_url == self.flask_url

    def test_linux(self):
        self.main_page.go_linux_page()

        assert self.driver.current_url == self.linux_url

    def test_centos(self):
        self.main_page.go_centos_page()

        assert self.driver.current_url == self.centos_url

    def test_network(self):
        self.main_page.go_network_page()

        assert self.driver.current_url == self.network_url

    def test_news(self):
        self.main_page.go_news_page()

        assert self.driver.current_url == self.wireshark_news_url

    def test_downloads(self):
        self.main_page.go_download_page()

        assert self.driver.current_url == self.wireshark_download_url

    def test_examples(self):
        self.main_page.go_examples()

        assert self.driver.current_url == self.tcpdump_examples_url

    def test_api(self):
        self.main_page.go_api()

        assert self.driver.current_url == self.api_url

    def test_future_of_internet(self):
        self.main_page.go_future_of_internet()

        assert self.driver.current_url == self.future_of_internet_url

    def test_smtp(self):
        self.main_page.go_smtp()

        assert self.driver.current_url == self.smtp_url
