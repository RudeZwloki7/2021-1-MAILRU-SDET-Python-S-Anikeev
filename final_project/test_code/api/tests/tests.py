import pytest

from base import ApiBase


@pytest.mark.smoke
class TestSmoke(ApiBase):
    authorize = False

    def test_status(self):
        response = self.api_client.get_status()

        assert response['status'] == 'ok'


@pytest.mark.API
class TestAddUser(ApiBase):

    def test_add_user(self):
        user = self.builder.create_user()
        self.api_client.post_add_user(user.username, user.password, user.email)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    def test_incorrect_username(self):
        user = self.builder.create_user(username=self.builder.random_letter())
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    def test_blank_pass(self):
        user = self.builder.create_user(password=' ')
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    def test_incorrect_email(self):
        user = self.builder.create_user(email=self.builder.random_letter() + '@mail.com')
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    def test_invalid_email(self):
        user = self.builder.create_user(email=self.builder.random_string())
        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.BAD_REQUEST)

        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)

    def test_existed_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)

        self.api_client.post_add_user(user.username, user.password, user.email,
                                      exp_status=self.api_client.status.NOT_CHANGED)

        self.mysql_client.delete_user(user.username)


@pytest.mark.API
class TestDeleteUser(ApiBase):

    def test_delete_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)

        self.api_client.get_delete_user(user.username)
        assert self.mysql_client.find_user(user.username) is None

    def test_delete_not_existed_user(self):
        user = self.builder.create_user()

        self.api_client.get_delete_user(user.username, exp_status=self.api_client.status.NOT_FOUND)
        assert self.mysql_client.find_user(user.username) is None


@pytest.mark.API
class TestBlockUser(ApiBase):

    def test_block_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_block_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_delete_user(user.username)

    def test_block_blocked_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user, access=0)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_block_user(user.username, exp_status=self.api_client.status.NOT_CHANGED)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_delete_user(user.username)

    def test_block_not_existed_user(self):
        user = self.builder.create_user()
        assert self.mysql_client.find_user(user.username) is None

        self.api_client.get_block_user(user.username, exp_status=self.api_client.status.NOT_FOUND)


@pytest.mark.API
class TestUnblockUser(ApiBase):

    def test_unblock_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user, access=0)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 0

        self.api_client.get_unblock_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_delete_user(user.username)

    def test_unblock_unblocked_user(self):
        user = self.builder.create_user()
        self.mysql_client.add_user(user)
        assert self.mysql_client.find_user(user.username)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_unblock_user(user.username, exp_status=self.api_client.status.NOT_CHANGED)
        assert self.mysql_client.find_user(user.username).access == 1

        self.api_client.get_delete_user(user.username)

    def test_unblock_not_existed_user(self):
        user = self.builder.create_user()
        assert self.mysql_client.find_user(user.username) is None

        self.api_client.get_unblock_user(user.username, exp_status=self.api_client.status.NOT_FOUND)
