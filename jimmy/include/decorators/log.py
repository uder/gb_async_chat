import traceback
import logging
from functools import wraps


def log(func):
    @wraps(func)
    def debug_log(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        logger: logging.Logger = self.logger
        # Get current level
        level = logger.getEffectiveLevel()
        logger.setLevel(logging.DEBUG)

        stack = traceback.extract_stack()
        stack.reverse()
        parent = stack[1]

        self.logger.debug(
            f'Call: {func.__name__} from {parent.name}("{parent.filename}:{parent.lineno}")')

        # Restore log level
        logger.setLevel(level)
        return result

    return debug_log
