import json
from dataclasses import dataclass

import faker
import requests

fake = faker.Faker()


@dataclass
class User:
    username: str = None
    email: str = None
    password: str = None
    password_repeat: str = None
    vk_id: str = None


class Builder:

    @staticmethod
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

        return User(username, email, password, password_repeat, vk_id)

    @staticmethod
    def random_letter():
        return fake.random_letter()

    @staticmethod
    def random_digit():
        return fake.random_letter()

    @staticmethod
    def random_string():
        return fake.pystr()
