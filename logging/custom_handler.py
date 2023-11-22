import logging
import logging.handlers
from abstracts import AbstractHandler

class CustomHandlerBuilder(AbstractHandler):
    """A builder class for creating different types of logging handlers.

    This class supports the creation of various logging handlers provided by
    the Python logging module. The type of handler is determined by the
    'handler_type' parameter passed to the constructor.

    Attributes:
        handler (logging.Handler): The handler instance created by the builder.
    """

    def __init__(self, handler_type, **kwargs):
        """Initializes the CustomHandlerBuilder with the specified handler type.

        Args:
            handler_type (str): The type of handler to create.
            **kwargs: Additional keyword arguments specific to the handler type.

        Raises:
            ValueError: If the handler_type is invalid or required parameters are missing.
        """
        if handler_type == "stream":
            self.handler = logging.StreamHandler()
        
        elif handler_type == "file":
            filename = kwargs.get('filename')
            self._validate_required('filename', filename)
            self.handler = logging.FileHandler(filename)
        
        elif handler_type == "rotating":
            filename = kwargs.get('filename')
            self._validate_required('filename', filename)
            maxBytes = kwargs.get('maxBytes', 1048576) # 1MB default
            backupCount = kwargs.get('backupCount', 5) # 5 files default
            self.handler = logging.handlers.RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
        
        elif handler_type == "timed_rotating":
            filename = kwargs.get('filename')
            self._validate_required('filename', filename)
            when = kwargs.get('when', 'D')
            backupCount = kwargs.get('backupCount', 5)
            self.handler = logging.handlers.TimedRotatingFileHandler(filename, when=when, backupCount=backupCount)
        
        elif handler_type == "socket":
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
            self.handler = logging.handlers.SocketHandler(host, port)
        
        elif handler_type == "http":
            host = kwargs.get('host', 'localhost')
            url = kwargs.get('url', '/log')
            method = kwargs.get('method', 'POST')
            self.handler = logging.handlers.HTTPHandler(host, url, method)
        
        elif handler_type == "smtp":
            mailhost = kwargs.get('mailhost', 'localhost')
            fromaddr = kwargs.get('fromaddr', 'log@example.com')
            toaddrs = kwargs.get('toaddrs', ['admin@example.com'])
            subject = kwargs.get('subject', 'Log Message')
            self.handler = logging.handlers.SMTPHandler(mailhost, fromaddr, toaddrs, subject)
        
        elif handler_type == "datagram":
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', logging.handlers.DEFAULT_UDP_LOGGING_PORT)
            self.handler = logging.handlers.DatagramHandler(host, port)
        
        elif handler_type == "memory":
            capacity = kwargs.get('capacity', 1024)
            flushLevel = kwargs.get('flushLevel', logging.ERROR)
            target = kwargs.get('target')
            self._validate_required('target', target)
            self.handler = logging.handlers.MemoryHandler(capacity, flushLevel, target)
        
        elif handler_type == "nt_event_log":
            appname = kwargs.get('appname', 'Python Application')
            dllname = kwargs.get('dllname')
            logtype = kwargs.get('logtype', 'Application')
            self.handler = logging.handlers.NTEventLogHandler(appname, dllname, logtype)
        
        elif handler_type == "queue":
            queue = kwargs.get('queue')
            self._validate_required('queue', queue)
            self.handler = logging.handlers.QueueHandler(queue)
        
        elif handler_type == "syslog":
            address = kwargs.get('address', ('localhost', logging.handlers.SYSLOG_UDP_PORT))
            facility = kwargs.get('facility', logging.handlers.SysLogHandler.LOG_USER)
            self.handler = logging.handlers.SysLogHandler(address, facility)
        
        elif handler_type == "watched_file":
            filename = kwargs.get('filename')
            self._validate_required('filename', filename)
            self.handler = logging.handlers.WatchedFileHandler(filename)
            
        else:
            raise ValueError("Invalid handler type")

    def _validate_required(self, param_name, param_value):
        """Validates that the required parameter is not None or empty.

        Args:
            param_name (str): The name of the parameter.
            param_value: The value of the parameter.

        Raises:
            ValueError: If the parameter value is None or empty.
        """
        if not param_value:
            raise ValueError(f"{param_name} is required for this handler type")

    def set_level(self, level):
        """Sets the logging level for the handler.

        Args:
            level (int): The logging level (e.g., logging.INFO, logging.DEBUG).

        Returns:
            CustomHandlerBuilder: The instance of the builder for chaining.
        """
        self.handler.setLevel(level)
        return self

    def set_formatter(self, formatter):
        """Sets the formatter for the handler.

        Args:
            formatter (logging.Formatter): The formatter to use with the handler.

        Returns:
            CustomHandlerBuilder: The instance of the builder for chaining.
        """
        self.handler.setFormatter(formatter)
        return self

    def build(self):
        """Builds and returns the configured logging handler.

        Returns:
            logging.Handler: The configured handler instance.
        """
        return self.handler
