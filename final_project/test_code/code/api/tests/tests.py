import allure
import pytest

from base import ApiBase


@pytest.mark.smoke
@allure.epic('Smoke tests')
@allure.feature('Проверка состояния приложения')
class TestSmoke(ApiBase):
    authorize = False

    @allure.story("Проверка состояния приложения по запросу")
    @allure.description("""
           Отправка API запроса на состояние приложения.
           Ожидается, что приложение запущени и вернет 
           статус 'ok' 
       """)
    def test_status(self):
        response = self.api_client.get_status()

        assert response['status'] == 'ok'


@pytest.mark.API
@allure.epic('API tests')
@allure.feature('Тестирование добавления нового пользователя')
class TestAddUser(ApiBase):

    @allure.story("Добавление нового пользователя с валидными данными")
    @allure.description("""
            Тестирование добавления нового пользователя с валидными данными.
            1. Создается новый пользователь.
            2. Осуществляется запрос на добавление нового пользователя.
            3. Проверка, что пользователь создан и добавлен в БД.
            4. Удаление созданного пользователя из БД.
    """)
    def test_add_user(self):
        user = self.builder.create_user()
        self.api_client.post_add_user(user.username, user.password, user.email)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    @allure.story("Добавление нового пользователя с некорректным именем")
    @allure.description("""
            Тестирование добавления нового пользователя с некорректным именем.
            1. Создается новый пользователь с некорректным именем.
            2. Осуществляется запрос на добавление нового пользователя.
            Ожидается статус код ответа 400.
            3. Проверка, что пользователь не добавлен в БД.
    """)
    def test_incorrect_username(self):
        user = self.builder.create_user(username=self.builder.random_letter())
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username) is None

    @allure.story("Добавление нового пользователя с пустым паролем")
    @allure.description("""
            Тестирование добавления нового пользователя с пустой строкой 
            в качестве пароля.
            1. Создается новый пользователь с пустым паролем.
            2. Осуществляется запрос на добавление нового пользователя.
            Ожидается статус код ответа 400.
            3. Проверка, что пользователь не добавлен в БД.
    """)
    def test_blank_pass(self):
        user = self.builder.create_user(password=' ')
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username) is None

    @allure.story("Добавление нового пользователя с некорректным адресом почты")
    @allure.description("""
            Тестирование добавления нового пользователя с некорректной длиной
            адреса почты.
            1. Создается новый пользователь с некорректным адресом почты.
            2. Осуществляется запрос на добавление нового пользователя.
            Ожидается статус код ответа 400.
            3. Проверка, что пользователь не добавлен в БД.
    """)
    def test_incorrect_email(self):
        user = self.builder.create_user(email=self.builder.random_letter() + '@mail.com')
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username) is None

    @allure.story("Добавление нового пользователя с неверным форматом адреса почты")
    @allure.description("""
            Тестирование добавления нового пользователя с неверным форматом 
            адреса почты.
            1. Создается новый пользователь с неверным форматом адреса почты.
            2. Осуществляется запрос на добавление нового пользователя.
            Ожидается статус код ответа 400.
            3. Проверка, что пользователь не добавлен в БД.
    """)
    def test_invalid_email(self):
        user = self.builder.create_user(email=self.builder.random_string())
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username) is None

    @allure.story("Добавление существующего пользователя")
    @allure.description("""
            Тестирование добавления существующего пользователя.
            1. Создается новый пользователь.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на добавление нового пользователя.
            Ожидается статус код ответа 304.
            4. Удаление созданного пользователя из БД.
    """)
    def test_existed_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)

        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.NOT_CHANGED)

        self.mysql_client.delete_user(user.username)


@pytest.mark.API
@allure.epic('API tests')
@allure.feature('Тестирование удаления пользователя')
class TestDeleteUser(ApiBase):

    @allure.story("Удаление существующего пользователя")
    @allure.description("""
            Тестирование удаления существующего пользователя.
            1. Создается новый пользователь.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на удаление созданного пользователя.
            Ожидается статус код ответа 204.
            4. Проверка, что пользователь удален из БД.
    """)
    def test_delete_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)

        self.api_client.get_delete_user(user.username)
        assert self.mysql_client.find_user(user.username) is None

    @allure.story("Удаление несуществующего пользователя")
    @allure.description("""
            Тестирование удаления несуществующего пользователя.
            1. Создается новый пользователь.
            2. Осуществляется запрос на удаление созданного пользователя.
            Ожидается статус код ответа 404.
            3. Проверка, что пользователь удален из БД.
    """)
    def test_delete_not_existed_user(self):
        user = self.builder.create_user()

        self.api_client.get_delete_user(user.username, exp_status=self.api_client.status.NOT_FOUND)
        assert self.mysql_client.find_user(user.username) is None


@pytest.mark.API
@allure.epic('API tests')
@allure.feature('Тестирование блокировки пользователя')
class TestBlockUser(ApiBase):

    @allure.story("Блокировка существующего пользователя")
    @allure.description("""
            Тестирование блокировки существующего пользователя.
            1. Создается новый пользователь с доступом к сайту.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на блокировку созданного пользователя.
            Ожидается статус код ответа 200.
            4. Проверка, что пользователь не имеет доступа к сайту.
            5. Удаление пользователя из БД.
    """)
    def test_block_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_block_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_delete_user(user.username)

    @allure.story("Блокировка заблокированного пользователя")
    @allure.description("""
            Тестирование блокировки заблокированного пользователя.
            1. Создается новый пользователь без доступа к сайту.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на блокировку созданного пользователя.
            Ожидается статус код ответа 304.
            4. Проверка, что пользователь не имеет доступа к сайту.
            5. Удаление пользователя из БД.
    """)
    def test_block_blocked_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user, access=0)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_block_user(user.username, exp_status=self.api_client.status.NOT_CHANGED)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_delete_user(user.username)

    @allure.story("Блокировка несуществующего пользователя")
    @allure.description("""
            Тестирование блокировки несуществующего пользователя.
            1. Создается новый пользователь.
            2. Осуществляется запрос на блокировку созданного пользователя.
            Ожидается статус код ответа 404.
    """)
    def test_block_not_existed_user(self):
        user = self.builder.create_user()
        assert self.mysql_client.find_user(user.username) is None

        self.api_client.get_block_user(user.username, exp_status=self.api_client.status.NOT_FOUND)


@pytest.mark.API
@allure.epic('API tests')
@allure.feature('Тестирование разблокировки пользователя')
class TestUnblockUser(ApiBase):

    @allure.story("Разблокировка существующего пользователя")
    @allure.description("""
            Тестирование разблокировки существующего пользователя.
            1. Создается новый пользователь без доступа к сайту.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на разблокировку созданного пользователя.
            Ожидается статус код ответа 200.
            4. Проверка, что пользователь имеет доступ к сайту.
            5. Удаление пользователя из БД.
    """)
    def test_unblock_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user, access=0)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_unblock_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_delete_user(user.username)

    @allure.story("Разблокировка разблокированного пользователя")
    @allure.description("""
            Тестирование разблокировки разблокированного пользователя.
            1. Создается новый пользователь с доступом к сайту.
            2. Созданный пользователь добавляется в БД.
            3. Осуществляется запрос на разблокировку созданного пользователя.
            Ожидается статус код ответа 304.
            4. Проверка, что пользователь имеет доступ к сайту.
            5. Удаление пользователя из БД.
    """)
    def test_unblock_unblocked_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_unblock_user(user.username, exp_status=self.api_client.status.NOT_CHANGED)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_delete_user(user.username)

    @allure.story("Разблокировка несуществующего пользователя")
    @allure.description("""
            Тестирование разблокировки несуществующего пользователя.
            1. Создается новый пользователь.
            2. Осуществляется запрос на разблокировку созданного пользователя.
            Ожидается статус код ответа 404.
    """)
    def test_unblock_not_existed_user(self):
        user = self.builder.create_user()
        assert self.mysql_client.find_user(user.username) is None

        self.api_client.get_unblock_user(user.username, exp_status=self.api_client.status.NOT_FOUND)
