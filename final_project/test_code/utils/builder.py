from dataclasses import dataclass

import faker

fake = faker.Faker()


@dataclass
class User:
    username: str = None
    email: str = None
    password: str = None
    password_repeat: str = None
    vk_id: int = None


class Builder:

    @staticmethod
    def create_user(username=None, email=None, password=None, password_repeat=None):
        sample_user = fake.simple_profile()
        if username is None:
            username = sample_user['username']

        if email is None:
            email = sample_user['mail']

        if password is None:
            password = fake.pystr()

        if password_repeat is None:
            password_repeat = password

        return User(username, email, password, password_repeat)

    @staticmethod
    def random_letter():
        return fake.random_letter()

    @staticmethod
    def random_digit():
        return fake.random_letter()

    @staticmethod
    def random_spec_char():
        return fake.random_letter()
