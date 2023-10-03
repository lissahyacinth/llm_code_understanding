from abc import abstractmethod


class Prompt:
    @abstractmethod
    def system_message(self, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def user_message(self, **kwargs) -> str:
        raise NotImplementedError
