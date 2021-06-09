import allure
import pytest
from ui.tests.base import BaseCase
from ui.str_values import MainPageUrls


@pytest.mark.UI
@allure.epic('UI tests')
@allure.feature('Тестирование страницы авторизации')
class TestLogin(BaseCase):
    is_authorized = False

    @allure.story("Авторизация с валидными данными")
    @allure.description("""
            Тестирование авторизации пользователя с валидными данными.
            1. Создается новый пользователь.
            2. Созданный пользователь добавляется в БД.
            3. Попытка авторизации пользователя.
            4. Проверка, что пользователь успешно авторизовался.
    """)
    def test_login(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(username=user.username)

        main_page = self.login_page.login(user.username, user.password)

        assert main_page.is_visible(main_page.locators.FOOTER_LOCATOR)
        assert self.driver.current_url == main_page.url
        assert user.vk_id in main_page.find(main_page.locators.VK_ID_LOCATOR).text

        self.mysql_client.delete_user(user.username)

    @allure.story("Авторизация с некорректной длиной имени пользователя")
    @allure.description("""
            Тестирование авторизации пользователя с некорректной длиной имени.
            1. Создается новый пользователь с некорректным именем.
            2. Попытка авторизации пользователя.
            3. Проверка, что пользователь не авторизовался и появилось
            корректное сообщение об ошибке.
    """)
    def test_incorrect_username_length_login(self):
        self.login_page.login(self.builder.random_letter(), self.builder.random_letter())

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    @allure.story("Авторизация с невалидными данными пользователя")
    @allure.description("""
            Тестирование авторизации пользователя с невалидными данными входа.
            1. Создается новый пользователь без добавления в БД.
            2. Попытка авторизации пользователя.
            3. Проверка, что пользователь не авторизовался и появилось 
               корректное сообщение об ошибке.
    """)
    def test_invalid_login(self):
        user = self.builder.create_user()
        self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Invalid username or password'

    @allure.story("Авторизация с пустой строкой пароля пользователя")
    @allure.description("""
            Тестирование авторизации пользователя с вводом пустой строки в качестве пароля.
            1. Создается новый пользователь без добавления в БД.
            2. Попытка авторизации пользователя.
            3. Проверка, что пользователь не авторизовался и появилось
               корректное сообщение об ошибке.
    """)
    def test_blank_pass_login(self):
        user = self.builder.create_user(password=' ')
        self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Необходимо указать пароль для авторизации'

    @allure.story("Авторизация пользователя с пустой строкой пароля и невалидным именем")
    @allure.description("""
            Тестирование авторизации пользователя с вводом пустой строки в 
            качестве пароля и неверного имени пользователя.
            1. Создается новый пользователь без добавления в БД.
            2. Попытка авторизации пользователя.
            3. Проверка, что пользователь не авторизовался и появилось
               корректное сообщение о первой возникшей ошибке.
    """)
    def test_invalid_login_and_passwd(self):
        user = self.builder.create_user(username=self.builder.random_letter(), password=' ')
        self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    @allure.story("Авторизация заблокированного пользователя")
    @allure.description("""
            Тестирование авторизации заблокированного пользователя.
            1. Создается новый пользователь.
            2. Пользователь добавляется в БД с access=0 (заблокирован).
            3. Попытка авторизации пользователя.
            4. Проверка, что пользователь не авторизовался и появилось
               корректное сообщение о первой возникшей ошибке.
    """)
    def test_blocked_user_login(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user=user, access=0)
        assert self.mysql_client.find_user(username=user.username)

        self.login_page.login(user.username, user.password)

        assert self.driver.current_url == self.login_page.url
        assert self.base_page.is_visible(
            self.base_page.locators.NOTIFICATION_LOCATOR).text == 'Ваша учетная запись заблокирована'

        self.mysql_client.delete_user(user.username)


@pytest.mark.UI
@allure.epic('UI tests')
@allure.feature('Тестирование страницы регистрации')
class TestRegistration(BaseCase):
    is_authorized = False

    @allure.story("Регистрация нового пользователя")
    @allure.description("""
            Тестирование регистрации нового пользователя.
            1. Создается новый пользователь.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь успешно зарегистрировался и был добавлен в БД.
            5. Удаление созданного пользователя из БД.
    """)
    def test_register(self):
        user = self.builder.create_user()
        reg_page = self.login_page.go_to_registration_page()
        main_page = reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username)
        assert self.driver.current_url == main_page.url

        self.mysql_client.delete_user(user.username)

    @allure.story("Регистрация нового пользователя с некорректным именем")
    @allure.description("""
            Тестирование регистрации нового пользователя с некорректным именем.
            1. Создается новый пользователь с некорректной длиной имени.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_incorrect_username_length(self):
        user = self.builder.create_user(username=self.builder.random_letter())
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    @allure.story("Регистрация нового пользователя с некорректной длиной адреса почты")
    @allure.description("""
            Тестирование регистрации нового пользователя с некорректной длиной адреса почты.
            1. Создается новый пользователь с некорректной длиной адреса почты.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_incorrect_email_length(self):
        user = self.builder.create_user(email=self.builder.random_letter())
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect email length'

    @allure.story("Регистрация нового пользователя с некорректной длиной адреса почты и имени")
    @allure.description("""
            Тестирование регистрации нового пользователя с некорректной длиной 
            адреса почты и имени пользователя.
            1. Создается новый пользователь с некорректной длиной адреса 
            почты и имени.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_incorrect_username_and_email(self):
        user = self.builder.create_user(username=self.builder.random_letter(),
                                        email=self.builder.random_letter())

        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Incorrect username length'

    @allure.story("Регистрация нового пользователя с пустой строкой в пароле")
    @allure.description("""
            Тестирование регистрации нового пользователя с пустой строкой в качестве пароля.
            1. Создается новый пользователь с с пустой строкой в качестве пароля.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_blank_pass_reg(self):
        user = self.builder.create_user(password=' ')
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(
            reg_page.locators.NOTIFICATION_LOCATOR).text == 'Необходимо указать пароль для регистрации'

    @allure.story("Регистрация нового пользователя с неверным форматом адреса почты")
    @allure.description("""
            Тестирование регистрации нового пользователя с неверным форматом адреса почты.
            1. Создается новый пользователь с неверным форматом адреса почты.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_invalid_email(self):
        user = self.builder.create_user(email=self.builder.random_string())
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Invalid email address'

    @allure.story("Регистрация нового пользователя с несовпадающим паролем")
    @allure.description("""
            Тестирование регистрации нового пользователя с несовпадающим паролем в строке
            подтверждения пароля.
            1. Создается новый пользователь с разными значениями пароля и его подтверждения.
            2. Осуществляется переход на страницу регистрации.
            3. Вводятся данные пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован, 
               не был добавлен в БД, и появилось корректное сообщение об ошибке.
    """)
    def test_unmatch_pass(self):
        user = self.builder.create_user(password_repeat=self.builder.random_digit())
        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(user.username, user.email, user.password, user.password_repeat)

        assert self.mysql_client.find_user(user.username) is None
        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'Passwords must match'

    @allure.story("Регистрация существующего пользователя")
    @allure.description("""
            Тестирование попытки регистрации существующего пользователя.
            1. Создается новый пользователь.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется переход на страницу регистрации.
            4. Создается еще один пользователь с данными, совпадающими частично/полностью
               с данными существующего пользователя.
            3. Вводятся данные второго пользователя для регистрации.
            4. Проверка, что пользователь не был зарегистрирован и появилось 
               корректное сообщение об ошибке.
    """)
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
        self.mysql_client.delete_user(username='test_qa')
        self.mysql_client.delete_user(email='qa_test@mail.com')

        user = self.builder.create_user(username='test_qa',
                                        email='qa_test@mail.com')

        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(username=user.username)

        reg_page = self.login_page.go_to_registration_page()
        reg_page.register_user(username, email, user.password, user.password_repeat)

        assert self.driver.current_url == reg_page.url
        assert reg_page.is_visible(reg_page.locators.NOTIFICATION_LOCATOR).text == 'User already exist'

        self.mysql_client.delete_user(user.username)


@pytest.mark.UI
@allure.epic('UI tests')
@allure.feature('Тестирование главной страницы приложения')
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

    @allure.story("Переход на страницу Python")
    @allure.description("""
            Попытка перехода на страницу Python кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_python(self):
        self.main_page.go_python_page()

        assert self.driver.current_url == self.urls.PYTHON_URL

    @allure.story("Переход на страницу Python History")
    @allure.description("""
            Попытка перехода на страницу Python History кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_python_history(self):
        self.main_page.go_python_history_page()

        assert self.driver.current_url == self.urls.PY_HISTORY_URL

    @allure.story("Переход на страницу Flask")
    @allure.description("""
            Попытка перехода на страницу Flask кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_flask(self):
        self.main_page.go_flask_page()
        assert self.driver.current_url == self.urls.FLASK_URL

    @allure.story("Переход на страницу Linux")
    @allure.description("""
            Попытка перехода на страницу Linux кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_linux(self):
        self.main_page.go_linux_page()

        assert self.driver.current_url == self.urls.LINUX_URL

    @allure.story("Переход на страницу Centos")
    @allure.description("""
            Попытка перехода на страницу Centos кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_centos(self):
        self.main_page.go_centos_page()

        assert self.driver.current_url == self.urls.CENTOS_URL

    @allure.story("Переход на страницу Network")
    @allure.description("""
            Попытка перехода на страницу Network кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_network(self):
        self.main_page.go_network_page()

        assert self.driver.current_url == self.urls.NETWORK_URL

    @allure.story("Переход на страницу Wireshark News")
    @allure.description("""
            Попытка перехода на страницу Wireshark News кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_news(self):
        self.main_page.go_news_page()

        assert self.driver.current_url == self.urls.WIRESHARK_NEWS_URL

    @allure.story("Переход на страницу Wireshark Downloads")
    @allure.description("""
            Попытка перехода на страницу Wireshark Downloads кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_downloads(self):
        self.main_page.go_download_page()

        assert self.driver.current_url == self.urls.WIRESHARK_DOWNLOAD_URL

    @allure.story("Переход на страницу TCPDUMP Examples")
    @allure.description("""
            Попытка перехода на страницу TCPDUMP Examples кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_examples(self):
        self.main_page.go_examples()

        assert self.driver.current_url == self.urls.TCPDUMP_EXAMPLES_URL

    @allure.story("Переход на страницу API")
    @allure.description("""
            Попытка перехода на страницу API кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_api(self):
        self.main_page.go_api()

        assert self.driver.current_url == self.urls.API_URL

    @allure.story("Переход на страницу Future of internet")
    @allure.description("""
            Попытка перехода на страницу Future of internet кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_future_of_internet(self):
        self.main_page.go_future_of_internet()

        assert self.driver.current_url == self.urls.FUTURE_OF_INTERNET_URL

    @allure.story("Переход на страницу SMTP")
    @allure.description("""
            Попытка перехода на страницу SMTP кликом по ссылке.
            Ожидается переход на корректный ресурс.
    """)
    def test_smtp(self):
        self.main_page.go_smtp()

        assert self.driver.current_url == self.urls.SMTP_URL

    @allure.story("Выход из аккаунта пользователя")
    @allure.description("""
            Попытка выхода из аккаунта пользователя кликом по кнопке выхода.
            Ожидается переход на страницу авторизации.
    """)
    def test_logout(self):
        self.main_page.logout()
        user = self.mysql_client.find_user('test_user')

        assert user.active == 0
        assert self.driver.current_url == self.login_page.url
