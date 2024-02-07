import faker


class MockUserRepository:
    def __init__(self, user):
        self.fake = faker.Faker()
        self.user = user

    async def insert(self, data: dict):
        return self.fake.pyint()

    async def update_by_filters(self, data: dict, **filters):
        ...

    async def update_by_id(self, data: dict, record_id: int):
        return self.fake.pyint()

    async def get_by_filters(self, **filters):
        return [self.user]

    async def get_all(self):
        return [self.user]

    async def get_by_id(self, record_id: int):
        return self.user

    async def delete_by_filters(self, **filters):
        ...

    async def delete_by_id(self, record_id: int):
        return self.fake.pyint()

    async def get_by_username(self, username: str):
        return self.user
