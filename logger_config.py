from datetime import datetime
from loguru import logger
import sys
import os
import warnings

class LoggerSetup:
    FILE_LOG_FORMAT = "<white>[{time:YYYY-MM-DD HH:mm:ss}</white>] | <level>{level: <8}</level> | <white>{message}</white>"
    CONSOLE_LOG_FORMAT = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>"

    def __init__(self, debug_enabled: bool = True):
        logger.remove()
        log_file_name = f'{datetime.now().strftime("%d-%m-%Y")}.log'

        # Create logs directory if it doesn't exist
        log_dir = 'logs/bot_logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, log_file_name)
        logger.add(log_file_path, format=self.FILE_LOG_FORMAT, level="DEBUG", rotation='1 day')

        logger.add(sys.stderr, colorize=True, format=self.CONSOLE_LOG_FORMAT,
                   level='DEBUG' if debug_enabled else 'INFO')

        # Redirect warnings to loguru
        self.redirect_warnings()

    def redirect_warnings(self):
        # Redirect all warnings to loguru
        def warning_formatter(message, category, filename, lineno, file=None, line=None):
            return f'{filename}:{lineno}: {category.__name__}: {message}'

        warnings.formatwarning = warning_formatter
        warnings.simplefilter('default')
        warnings.showwarning = self._log_warning

    def _log_warning(self, message, category, filename, lineno, file=None, line=None):
        logger.warning(f'{filename}:{lineno}: {category.__name__}: {message}')

# Initialize logger
LoggerSetup(debug_enabled=True)
