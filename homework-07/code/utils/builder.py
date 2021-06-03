from dataclasses import dataclass

import faker

fake = faker.Faker()


@dataclass
class User:
    name: str = None
    surname: str = None
    new_surname: str = None
    user_id: int = None


class Builder:

    @staticmethod
    def create_user(name=None, surname=None, new_surname=None, user_id=None):

        if name is None:
            name = fake.first_name()

        if surname is None:
            surname = fake.last_name()

        if new_surname is None:
            new_surname = fake.last_name()

        if user_id is None:
            user_id = fake.random_int()

        return User(name, surname, new_surname, user_id)
