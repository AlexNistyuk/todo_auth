import faker
import pytest

from infrastructure.config import get_settings

settings = get_settings()


class TestTokenRefresh:
    url = "api/v1/token/refresh/"

    @pytest.mark.asyncio
    async def test_refresh_ok(self, client, mock_user_repo_user, tokens):
        response = client.post(
            url=self.url, params={"refresh_token": tokens["refresh_token"]}
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get("refresh_token")
        assert response.json().get("access_token")

    @pytest.mark.asyncio
    async def test_refresh_using_access_token(
        self, client, mock_user_repo_user, tokens
    ):
        response = client.post(
            url=self.url, params={"refresh_token": tokens["access_token"]}
        )

        assert response.status_code == 401


class TestTokenVerify:
    url = "api/v1/token/verify/"

    def setup_method(self):
        self.fake = faker.Faker()

    @pytest.mark.asyncio
    async def test_verify_ok(self, client, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_verify_incorrect_auth_keyword(self, client, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{self.fake.user_name()} {tokens['access_token']}"
            },
        )

        assert response.status_code == 401


class TestTokenUserInfo:
    url = "api/v1/token/user-info/"

    def setup_method(self):
        self.fake = faker.Faker()

    @pytest.mark.asyncio
    async def test_user_info_ok(self, client, mock_user_repo_user, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get("id")

    @pytest.mark.asyncio
    async def test_user_info_using_refresh_token(self, client, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['refresh_token']}"
            },
        )

        assert response.status_code == 401
