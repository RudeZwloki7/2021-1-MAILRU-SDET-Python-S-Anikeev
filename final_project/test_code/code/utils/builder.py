import logging
from dataclasses import dataclass
import allure
import faker

fake = faker.Faker()
logger = logging.getLogger('test')


@dataclass
class User:
    username: str = None
    email: str = None
    password: str = None
    password_repeat: str = None
    vk_id: str = None


class Builder:

    @staticmethod
    @allure.step('Create new User')
    def create_user(username=None, email=None, password=None, password_repeat=None, vk_id=None):
        sample_user = fake.simple_profile()
        if username is None:
            username = sample_user['username'][:15:]

        if email is None:
            email = sample_user['mail']

        if password is None:
            password = fake.pystr()

        if password_repeat is None:
            password_repeat = password

        if vk_id is None:
            vk_id = fake.bothify(text='????##')

        user = User(username, email, password, password_repeat, vk_id)
        logger.debug(f'Create new user {user}')
        return user

    @staticmethod
    def random_letter():
        return fake.random_letter()

    @staticmethod
    def random_digit():
        return fake.random_letter()

    @staticmethod
    def random_string():
        return fake.pystr()
