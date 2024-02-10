import datetime

import faker


class UserFactory:
    def __init__(self, user_role):
        self.user_role = user_role
        self.fake = faker.Faker()

    @property
    def id(self):
        return self.fake.pyint()

    @property
    def username(self):
        return self.fake.user_name()

    @property
    def password(self):
        return self.fake.password()

    @property
    def role(self):
        return self.user_role

    @property
    def created_at(self):
        return datetime.datetime.now()

    @property
    def updated_at(self):
        return datetime.datetime.now()
