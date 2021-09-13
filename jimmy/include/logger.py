import abc
import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class LoggerMixin:
    @staticmethod
    def _get_logger(logname: str, logdir: str, logfile: str, loglevel: str, **kwargs) -> logging.Logger:
        logger_builder = JimmyLoggerBuilder()
        logger = logger_builder.create_logger(logname, logdir, logfile, loglevel, **kwargs)

        return logger


class HandlerBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, *args, **kwargs) -> logging.Handler:
        pass


class FileHandlerBuilder(HandlerBuilder):
    def create(self, logdir: str, logfile: str, **kwargs) -> logging.FileHandler:
        self._prepare_directory(logdir)
        logpath = os.path.join(logdir, logfile)
        handler = logging.FileHandler(filename=logpath)

        return handler

    def _prepare_directory(self, logdir: str) -> None:
        os.makedirs(logdir, exist_ok=True)


class RotatedFileHandlerBuilder(FileHandlerBuilder):
    def create(self, logdir: str, logfile: str, max_bytes: int = 1024, **kwargs) -> RotatingFileHandler:
        self._prepare_directory(logdir)
        logpath = os.path.join(logdir, logfile)
        handler = RotatingFileHandler(filename=logpath, maxBytes=max_bytes, backupCount=1)

        return handler


class TimedRotatingFileHandlerBuilder(FileHandlerBuilder):
    def create(self, logdir: str, logfile: str, **kwargs) -> TimedRotatingFileHandler:
        self._prepare_directory(logdir)
        logpath = os.path.join(logdir, logfile)
        handler = TimedRotatingFileHandler(logpath, backupCount=1, interval=1, when='h')

        return handler


class JimmyLoggerBuilder:
    _handlers = {
        'file': FileHandlerBuilder(),
        'rotated_file': RotatedFileHandlerBuilder(),
        'timed_file': TimedRotatingFileHandlerBuilder(),
    }

    def create_logger(self, logname: str, logdir: str, logfile: str, loglevel: str, **kwargs) -> logging.Logger:
        formatter = self._get_formatter(logname)
        handler = self._get_handler(logname, logdir, logfile, **kwargs)
        handler.setFormatter(formatter)
        logger = logging.getLogger(logname)
        logger.addHandler(handler)
        logger.setLevel(loglevel)

        return logger

    def _get_handler_creator(self, handler_type: str) -> HandlerBuilder:
        handler_builder = self._handlers.get(handler_type)
        return handler_builder

    def _get_handler(self, logname: str, logdir: str, logfile: str, **kwargs) -> logging.Handler:
        handler_type = 'file'
        if logname == 'server':
            handler_type = 'timed_file'
        elif logname == 'client':
            handler_type = 'file'

        handler_builder = self._get_handler_creator(handler_type)

        handler = handler_builder.create(logdir, logfile, **kwargs)

        return handler

    def _get_formatter(self, logname: str) -> logging.Formatter:
        logformat = f'%(asctime)s %(levelname)s {logname}::%(module)s::%(funcName)s: %(message)s'
        formatter = logging.Formatter(logformat)

        return formatter
