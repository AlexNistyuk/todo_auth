import faker
import pytest

from tests.conftest import client


class TestAuthRegister:
    url = "api/v1/auth/register"

    def setup_method(self):
        self.fake = faker.Faker()

    @pytest.mark.asyncio
    async def test_register_ok(self, mock_user_repo_user):
        response = client.post(
            url=self.url,
            json={"username": self.fake.user_name(), "password": self.fake.password()},
        )

        assert response.status_code == 201
        assert isinstance(response.json(), dict)
        assert isinstance(response.json()["id"], int)

    @pytest.mark.asyncio
    async def test_register_without_username(self):
        response = client.post(url=self.url, json={"password": self.fake.password()})

        assert response.status_code == 422


class TestAuthLogin:
    url = "api/v1/auth/login"

    def setup_method(self):
        self.fake = faker.Faker()

    @pytest.mark.asyncio
    async def test_login_ok(self, mock_user_service_verify):
        response = client.post(
            url=self.url,
            json={"username": self.fake.user_name(), "password": self.fake.password()},
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get("access_token")
        assert response.json().get("refresh_token")

    @pytest.mark.asyncio
    async def test_login_without_username(self):
        response = client.post(url=self.url, json={"password": self.fake.password()})

        assert response.status_code == 422
