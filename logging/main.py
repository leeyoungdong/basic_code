from custom_logger import CustomLogger
from custom_handler import CustomHandlerBuilder
from custom_formatter import CustomFormatterFactory
import logging
import pytz

class ErrorFilter(logging.Filter):
    def __init__(self, level=logging.ERROR, message_contains=None, module_name=None):
        self.level = level
        self.message_contains = message_contains
        self.module_name = module_name

    def filter(self, record):
        if record.levelno < self.level:
            return False

        if self.message_contains and self.message_contains not in record.getMessage():
            return False

        if self.module_name and record.module != self.module_name:
            return False

        return True

    
def setup_loggers():
    # Logger 1: File logger with standard formatter
    file_logger = CustomLogger.create_logger(name='FileLogger', level=logging.INFO)
    file_formatter = CustomFormatterFactory.standard_formatter()
    file_handler = CustomHandlerBuilder('file', filename='info_log.log').set_formatter(file_formatter).set_level(logging.INFO).build()
    file_logger.add_handler(file_handler)

    # Logger 2: Stream logger with simple formatter
    stream_logger = CustomLogger.create_logger(name='StreamLogger', level=logging.WARNING)
    stream_formatter = CustomFormatterFactory.simple_formatter()
    stream_handler = CustomHandlerBuilder('stream').set_formatter(stream_formatter).set_level(logging.WARNING).build()
    stream_logger.add_handler(stream_handler)

    # Logger 3: File logger with Apache-style formatter
    apache_logger = CustomLogger.create_logger(name='ApacheLogger', level=logging.DEBUG)
    apache_formatter = CustomFormatterFactory.apache_formatter()
    apache_handler = CustomHandlerBuilder('file', filename='apache_log.log').set_formatter(apache_formatter).set_level(logging.DEBUG).build()
    apache_logger.add_handler(apache_handler)

    return file_logger, stream_logger, apache_logger

def main():
    file_logger, stream_logger, apache_logger = setup_loggers()

    file_logger.info("This is an info message for the file logger.")
    stream_logger.warning("This is a warning message for the stream logger.")
    apache_logger.debug("This is a debug message for the apache logger.")


if __name__ == "__main__":
    main()
