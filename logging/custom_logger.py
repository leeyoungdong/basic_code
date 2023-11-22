import logging
from abstracts import AbstractLogger

class CustomLogger(AbstractLogger):
    """
    A custom logger class extending the AbstractLogger. It provides an interface to create and manage logging instances.

    This class wraps the standard Python logging.Logger object, providing additional convenience methods for creating, configuring, and using loggers in an application.

    Attributes:
        logger (logging.Logger): The encapsulated logger instance.
    """

    def __init__(self, name=None, level=logging.INFO):
        """
        Initializes a new instance of the CustomLogger.

        Args:
            name (str, optional): The name of the logger. Defaults to None, which creates a root logger.
            level (int, optional): The initial logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.set_level(level)

    @classmethod
    def create_logger(cls, name=None, level=logging.INFO):
        """
        Class method to create a new logger instance.

        Args:
            name (str, optional): The name of the logger.
            level (int, optional): The logging level.

        Returns:
            CustomLogger: A new instance of CustomLogger.
        """
        return cls(name, level)

    def set_level(self, level):
        self.logger.setLevel(level)

    def add_handler(self, handler):
        self.logger.addHandler(handler)

    def remove_handler(self, handler):
        self.logger.removeHandler(handler)

    def add_filter(self, filter):
        self.logger.addFilter(filter)

    def remove_filter(self, filter):
        self.logger.removeFilter(filter)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
    
    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)

    def fatal(self, message, *args, **kwargs):
        self.logger.fatal(message, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    def isEnabledFor(self, level):
        """
        Checks if this logger is enabled for the specified level.

        Args:
            level (int): The level to check against the logger's level.

        Returns:
            bool: True if the logger is enabled for the specified level, False otherwise.
        """
        return self.logger.isEnabledFor(level)

    def getChild(self, suffix):
        """
        Gets a child logger relative to this logger.

        Args:
            suffix (str): The suffix for the child logger's name.

        Returns:
            logging.Logger: A child logger with a name appended with the suffix.
        """
        return self.logger.getChild(suffix)

    def getEffectiveLevel(self):
        """
        Gets the effective level for this logger.

        Returns:
            int: The effective logging level for this logger.
        """
        return self.logger.getEffectiveLevel()

    def hasHandlers(self):
        """
        Checks if this logger has any handlers configured.

        Returns:
            bool: True if the logger has handlers, False otherwise.
        """
        return self.logger.hasHandlers()
    
    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Finds the caller's details such as filename and line number.

        Args:
            stack_info (bool, optional): If True, stack info is included. Defaults to False.
            stacklevel (int, optional): The stack level. Defaults to 1.

        Returns:
            tuple: A tuple containing information about the caller.
        """
        return self.logger.findCaller(stack_info, stacklevel)

    def handle(self, record):
        """
        Handles the specified record by passing it to all relevant handlers.

        Args:
            record (logging.LogRecord): The log record to be handled.
        """
        self.logger.handle(record)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        Creates a LogRecord instance with the specified information.

        Args:
            name (str): The name of the logger.
            level (int): The logging level.
            fn (str): Filename where the log call was made.
            lno (int): Line number where the log call was made.
            msg (str): The log message.
            args (tuple): Arguments to be merged into msg.
            exc_info (tuple or None): Exception tuple (e.g., from sys.exc_info()) or None.
            func (str, optional): Function name where the log call was made.
            extra (dict, optional): Extra information to add to the log record.
            sinfo (str, optional): Stack info.

        Returns:
            logging.LogRecord: The created LogRecord instance.
        """
        return self.logger.makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

    def callHandlers(self, record):
        """
        Passes a record to all relevant handlers.

        This method is used for passing a record to all handlers interested in it
        until it is handled by a suitable handler.

        Args:
            record (logging.LogRecord): The log record to be handled.
        """
        self.logger.callHandlers(record)
        
    def filter(self, record):
        """
        Applies the logger's filters to the record.

        Args:
            record (logging.LogRecord): The log record to filter.

        Returns:
            bool: True if the record should be logged, False otherwise.
        """
        return self.logger.filter(record)