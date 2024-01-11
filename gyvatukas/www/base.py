import abc


class BaseClient(abc.ABC):
    """Base client to build WWW clients on top of.

    We want to be nice to the APIs and websites, so we implement rate limiting.
    """

    def __init__(self, rate_limit_per_second):
        self.rate_limit_per_second = rate_limit_per_second

    @abc.abstractmethod
    def rate_limit(self) -> None:
        pass
