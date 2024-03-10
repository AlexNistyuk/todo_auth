import faker
import pytest

from infrastructure.config import get_settings

settings = get_settings()


class TestUsers:
    url = "api/v1/users/"

    def setup_method(self):
        self.fake = faker.Faker()

    @pytest.mark.asyncio
    async def test_list_ok(self, client, mock_user_repo_admin, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert isinstance(response.json()[0], dict)

    @pytest.mark.asyncio
    async def test_list_permission_denied(self, client, mock_user_repo_user, tokens):
        response = client.get(
            url=self.url,
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_retrieve_ok(self, client, mock_user_repo_admin, tokens):
        response = client.get(
            url=self.url + f"{self.fake.pyint()}/",
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized(self, client, tokens):
        response = client.get(
            url=self.url + f"{self.fake.pyint()}/",
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['refresh_token']}"
            },
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_ok(self, client, mock_user_repo_admin, tokens):
        response = client.delete(
            url=self.url + f"{self.fake.pyint()}/",
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_permission_denied(self, client, mock_user_repo_user, tokens):
        response = client.delete(
            url=self.url + f"{self.fake.pyint()}/",
            headers={
                settings.http_auth_header: f"{settings.http_auth_keyword} {tokens['access_token']}"
            },
        )

        assert response.status_code == 403
