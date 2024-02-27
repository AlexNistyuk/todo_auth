from starlette.requests import Request

from domain.exceptions.users import UserPermissionDenied
from infrastructure.permissions.interfaces import IPermission


class BasePermission(IPermission):
    """Base permission"""

    async def __call__(self, request: Request):
        user_role = request.state.user.role.value

        result = await self.has_permission(user_role)
        if not result:
            raise UserPermissionDenied
        return self
