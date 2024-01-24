from abc import ABC, abstractmethod


class IPermission(ABC):
    @abstractmethod
    async def has_permission(self, *args, **kwargs):
        raise NotImplementedError
