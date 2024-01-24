from infrastructure.config import get_settings
from infrastructure.models.users import UserRole
from infrastructure.permissions.base import BasePermission

settings = get_settings()


class IsUser(BasePermission):
    async def has_permission(self, user_role: str) -> bool:
        return user_role == UserRole.user.value


class IsAdmin(BasePermission):
    async def has_permission(self, user_role: str) -> bool:
        return user_role == UserRole.admin.value


class IsUserOrAdmin(BasePermission):
    async def has_permission(self, user_role: str) -> bool:
        return user_role in {UserRole.user.value, UserRole.admin.value}
