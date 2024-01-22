from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """Abstract unit of work"""

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self, *args, **kwargs):
        raise NotImplementedError
