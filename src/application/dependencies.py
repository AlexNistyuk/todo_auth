from dependency_injector import containers, providers

from application.use_cases.interfaces import IUseCase
from application.use_cases.token import TokenUseCase
from application.use_cases.users import UserUseCase
from infrastructure.uow.base import UnitOfWork
from infrastructure.uow.interfaces import IUnitOfWork


class Container(containers.DeclarativeContainer):
    uow: IUnitOfWork = providers.Factory(UnitOfWork)
    user_use_case: IUseCase = providers.Factory(UserUseCase, uow)
    token_use_case: TokenUseCase = providers.Factory(TokenUseCase, user_use_case)
