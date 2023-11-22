from abc import ABC, abstractmethod

class AbstractFormatter(ABC):
    @abstractmethod
    def create_formatter(self, fmt, datefmt, style):
        pass

class AbstractLogger(ABC):
    @abstractmethod
    def set_level(self, level):
        pass

    @abstractmethod
    def add_handler(self, handler):
        pass

    @abstractmethod
    def remove_handler(self, handler):
        pass

    @abstractmethod
    def add_filter(self, filter):
        pass

    @abstractmethod
    def remove_filter(self, filter):
        pass

class AbstractHandler(ABC):
    @abstractmethod
    def set_level(self, level):
        pass

    @abstractmethod
    def set_formatter(self, formatter):
        pass

    @abstractmethod
    def build(self):
        pass
