import faker
import pytest
from starlette.testclient import TestClient

from domain.utils.token import Token
from infrastructure.models.users import UserRole
from main import app
from tests.factories import UserFactory

client = TestClient(app=app)
fake = faker.Faker()


def mock_user_repo(user, mocker):
    repo_path = "infrastructure.repositories.users.UserRepository"

    mocker.patch(f"{repo_path}.insert", return_value=fake.pyint())
    mocker.patch(f"{repo_path}.update_by_id", return_value=fake.pyint())
    mocker.patch(f"{repo_path}.get_by_filters", return_value=[user])
    mocker.patch(f"{repo_path}.get_all", return_value=[user])
    mocker.patch(f"{repo_path}.get_by_id", return_value=user)
    mocker.patch(f"{repo_path}.delete_by_id", return_value=fake.pyint())
    mocker.patch(f"{repo_path}.get_by_username", return_value=user)


@pytest.fixture()
async def mock_user_repo_user(mocker):
    user = UserFactory(user_role=UserRole.user)
    mock_user_repo(user, mocker)


@pytest.fixture()
async def mock_user_repo_admin(mocker):
    user = UserFactory(user_role=UserRole.admin)
    mock_user_repo(user, mocker)


@pytest.fixture()
async def mock_user_service_verify(mocker):
    user = UserFactory(UserRole.user)
    mocker.patch("application.use_cases.users.UserUseCase.verify", return_value=user)


@pytest.fixture()
def tokens():
    return Token(fake.pyint()).get_tokens()
