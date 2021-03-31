import pytest
from base import User


class TestOne(User):
    @pytest.mark.smoke()
    def test_title(self):
        assert 'Рекламная платформа myTarget — Сервис таргетированной рекламы' in self.driver.title

    @pytest.mark.UI()
    def test_login(self, login):
        assert '/dashboard' in self.driver.current_url

    @pytest.mark.UI()
    def test_logout(self, login):
        self.user_logout()
        assert 'Рекламная платформа myTarget — Сервис таргетированной рекламы' in self.driver.title
        assert 'https://target.my.com/' == self.driver.current_url

    @pytest.mark.UI()
    def test_edit_profile(self, login):
        answer = self.user_edit_profile()
        assert 'Контактная информация' in self.driver.title
        assert 'Информация успешно сохранена' in answer

    @pytest.mark.UI()
    @pytest.mark.parametrize(
        'btn_name, expected_url',
        [
            pytest.param(
                'Баланс',
                'https://target.my.com/billing'
            ),
            pytest.param(
                'Статистика',
                'https://target.my.com/statistics'
            )
        ]
    )
    def test_navigation(self, login, btn_name, expected_url):
        self.user_navigate(btn_name)
        assert expected_url in self.driver.current_url
