import logging
import pytz
from datetime import datetime
from abstracts import AbstractFormatter


class CustomFormatter(logging.Formatter):
    """
    CustomFormatter extends the standard logging.Formatter to support timezones and custom time formats.

    Attributes:
        tz (datetime.tzinfo): Timezone information for formatting the log record's time.
    """

    def __init__(self, fmt=None, datefmt=None, tz=pytz.timezone("Asia/Seoul")):
        """
        Initializes the CustomFormatter with a format, date format, and timezone.

        Args:
            fmt (str, optional): The log format string.
            datefmt (str, optional): The date format string.
            tz (datetime.tzinfo, optional): The timezone for log timestamps. Defaults to Asia/Seoul.
        """
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        """
        Formats the time of the log record as per the specified timezone and date format.

        Args:
            record (logging.LogRecord): The log record.
            datefmt (str, optional): The date format string.

        Returns:
            str: The formatted time string.
        """
        ct = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            try:
                s = ct.isoformat(timespec='milliseconds')
            except TypeError:
                s = ct.isoformat()
        return s
    
    def format(self, record):
        """
        Formats the log record.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """
        record.timezone = self.tz.zone 
        return super().format(record)
    
class CustomFormatterFactory(AbstractFormatter):
    """
    CustomFormatterFactory provides static methods to create different types of CustomFormatters.

    This factory class simplifies the creation of various formatter configurations.
    """

    @staticmethod
    def create_formatter(fmt=None, datefmt=None, tz=pytz.timezone("Asia/Seoul")):
        """
        Creates a CustomFormatter with specified format, date format, and timezone.

        Args:
            fmt (str, optional): The log format string.
            datefmt (str, optional): The date format string.
            tz (datetime.tzinfo, optional): The timezone for log timestamps.

        Returns:
            CustomFormatter: A new CustomFormatter instance.
        """
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)

    @staticmethod
    def full_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = (
            '%(asctime)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d - %(funcName)s] - '
            '(%(process)d - %(processName)s - %(thread)d - %(threadName)s) - '
            '%(name)s - %(module)s - %(pathname)s - '
            '%(message)s'
        )
        datefmt = '%Y-%m-%d %H:%M:%S'
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)
    
    @staticmethod
    def standard_formatter(tz=pytz.timezone("Asia/Seoul")):
        return CustomFormatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', tz=tz)

    @staticmethod
    def simple_formatter(tz=pytz.timezone("Asia/Seoul")):
        return CustomFormatter(fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', tz=tz)

    @staticmethod
    def page_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(timezone)s: %(message)s'
        return CustomFormatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S', tz=tz)
    
    @staticmethod
    def apache_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = '%(remote_host)s %(remote_logname)s %(remote_user)s [%(asctime)s] "%(request)s" %(status)s %(bytes_sent)s'
        datefmt = '%d/%b/%Y:%H:%M:%S %z'
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)

    @staticmethod
    def ms_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = '%(asctime)s %(source)s %(event_id)s %(event_type)s %(category)s [%(user)s]: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)

    @staticmethod
    def c_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] (%(funcName)s): %(message)s'
        datefmt = '%b %d %H:%M:%S'
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)

    @staticmethod
    def linux_syslog_formatter(tz=pytz.timezone("Asia/Seoul")):
        fmt = '%(asctime)s %(hostname)s %(tag)s[%(process)d]: %(message)s'
        datefmt = '%b %d %H:%M:%S'
        return CustomFormatter(fmt=fmt, datefmt=datefmt, tz=tz)