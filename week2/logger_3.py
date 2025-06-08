import sys
from datetime import datetime
from abc import ABC, abstractmethod

class Formatter(ABC):
    @abstractmethod
    def format(self, message):
        pass

class TimestampFormatter(Formatter):
    def __init__(self, time_format):
        self.time_format = time_format

    def format(self, message):
        timestamp = datetime.now().strftime(f"[{self.time_format}]")
        return f"{timestamp} {message}"

class Handler:
    def __init__(self, out_stream):
        self.out_stream = out_stream

    def handle(self, message):
        print(message, file=self.out_stream)

class Logger:
    def __init__(self, formatter: Formatter):
        self.formatter = formatter
        self.handlers = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)
        return self

    def log(self, message):
        formatted_message = self.formatter.format(message)
        for handler in self.handlers:
            handler.handle(formatted_message)

formatter = TimestampFormatter("%Y-%m-%d %H:%M:%S")
logger = Logger(formatter)
logger.add_handler(Handler(sys.stderr))
logger.add_handler(Handler(sys.stdout))
logger.log("Test log message")