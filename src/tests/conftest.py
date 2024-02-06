import pytest
from starlette.testclient import TestClient

from domain.utils.token import Token
from infrastructure.models.users import UserRole
from main import app
from tests.factories import UserFactory
from tests.mock import MockUserRepository

client = TestClient(app=app)


def mock_user_repo(user, monkeypatch):
    mock_repo = MockUserRepository(user)
    repo_path = "infrastructure.repositories.users.UserRepository"

    monkeypatch.setattr(f"{repo_path}.insert", mock_repo.insert)
    monkeypatch.setattr(f"{repo_path}.update_by_filters", mock_repo.update_by_filters)
    monkeypatch.setattr(f"{repo_path}.update_by_id", mock_repo.update_by_id)
    monkeypatch.setattr(f"{repo_path}.get_by_filters", mock_repo.get_by_filters)
    monkeypatch.setattr(f"{repo_path}.get_all", mock_repo.get_all)
    monkeypatch.setattr(f"{repo_path}.get_by_id", mock_repo.get_by_id)
    monkeypatch.setattr(f"{repo_path}.delete_by_filters", mock_repo.delete_by_filters)
    monkeypatch.setattr(f"{repo_path}.delete_by_id", mock_repo.delete_by_id)
    monkeypatch.setattr(f"{repo_path}.get_by_username", mock_repo.get_by_username)


@pytest.fixture()
async def mock_user_repo_user(monkeypatch):
    user = UserFactory(user_role=UserRole.user)
    mock_user_repo(user, monkeypatch)


@pytest.fixture()
async def mock_user_repo_admin(monkeypatch):
    user = UserFactory(user_role=UserRole.admin)
    mock_user_repo(user, monkeypatch)


@pytest.fixture()
async def mock_user_service_verify(monkeypatch):
    async def mock_verify(*args, **kwargs):
        return UserFactory(UserRole.user)

    monkeypatch.setattr("application.use_cases.users.UserUseCase.verify", mock_verify)


@pytest.fixture()
async def admin_permission(monkeypatch):
    monkeypatch.setattr(
        "infrastructure.permissions.base.BasePermission.__get_user_role",
        lambda: "admin",
    )


@pytest.fixture()
def tokens(monkeypatch):
    user_id = 1

    return Token(user_id).get_tokens()
