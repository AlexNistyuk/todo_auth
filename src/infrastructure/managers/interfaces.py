from abc import ABC, abstractmethod


class IManager(ABC):
    """Abstract manager"""

    @abstractmethod
    async def connect(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def close(self, *args, **kwargs):
        raise NotImplementedError
