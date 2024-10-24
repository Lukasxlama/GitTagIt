##################################
# Project: GitTagIt             #
# Filename: LogManager.py        #
# Version: 1.0                   #
# Author: lukasxlama             #
##################################

### Imports ###
import logging
from logging import INFO, DEBUG, ERROR, CRITICAL, WARNING, Formatter, getLogger, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


### Classes ###
class LevelFilter(logging.Filter):
    def __init__(self, level: int) -> None:
        """
        Filters log messages by a specific log level.

        :param level: The log level to filter by.
        :return: None.
        """

        super().__init__()
        self.level: int = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level


class LogManager:
    """
    Manages logging configuration for the application.
    """

    initialized: bool = False
    logger: Optional[Logger] = None

    def __init__(self, logDir: Path = Path("../log")) -> None:
        """
        Initializes the LogManager and sets up logging handlers.

        :param logDir: The directory where log files will be stored.
        :return: None.
        """

        self.logDir: Path = logDir

        if not LogManager.initialized:
            self.setupLogging()
            LogManager.initialized = True

    def setupLogging(self) -> None:
        """
        Sets up the logging handlers for different log levels.

        :return: None
        """

        if LogManager.initialized:
            return

        try:
            self.logDir.mkdir(parents=True, exist_ok=True)

            LogManager.logger = getLogger('GitTagIt_LOGGER')
            LogManager.logger.setLevel(DEBUG)

            logFormatter = Formatter('%(asctime)s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

            # INFO Handler
            infoHandler = RotatingFileHandler(
                filename=self.logDir / 'info.log',
                maxBytes=5_242_880,
                backupCount=5,
                encoding='utf-8'
            )
            infoHandler.setLevel(INFO)
            infoHandler.setFormatter(logFormatter)
            infoHandler.addFilter(LevelFilter(INFO))
            LogManager.logger.addHandler(infoHandler)

            # DEBUG Handler
            debugHandler = RotatingFileHandler(
                filename=self.logDir / 'debug.log',
                maxBytes=5_242_880,
                backupCount=5,
                encoding='utf-8'
            )
            debugHandler.setLevel(DEBUG)
            debugHandler.setFormatter(logFormatter)
            debugHandler.addFilter(LevelFilter(DEBUG))
            LogManager.logger.addHandler(debugHandler)

            # ERROR Handler
            errorHandler = RotatingFileHandler(
                filename=self.logDir / 'error.log',
                maxBytes=5_242_880,
                backupCount=5,
                encoding='utf-8'
            )
            errorHandler.setLevel(ERROR)
            errorHandler.setFormatter(
                Formatter('%(asctime)s - ERROR: %(message)s\nStack Trace:\n%(exc_info)s\n', '%Y-%m-%d %H:%M:%S'))
            errorHandler.addFilter(LevelFilter(ERROR))
            LogManager.logger.addHandler(errorHandler)

            # CRITICAL Handler
            criticalHandler = RotatingFileHandler(
                filename=self.logDir / 'critical.log',
                maxBytes=5_242_880,
                backupCount=5,
                encoding='utf-8'
            )
            criticalHandler.setLevel(CRITICAL)
            criticalHandler.setFormatter(logFormatter)
            criticalHandler.addFilter(LevelFilter(CRITICAL))
            LogManager.logger.addHandler(criticalHandler)

            # WARNING Handler
            warningHandler = RotatingFileHandler(
                filename=self.logDir / 'warning.log',
                maxBytes=5_242_880,
                backupCount=5,
                encoding='utf-8'
            )
            warningHandler.setLevel(WARNING)
            warningHandler.setFormatter(logFormatter)
            warningHandler.addFilter(LevelFilter(WARNING))
            LogManager.logger.addHandler(warningHandler)

        except Exception as ERR_01:
            print(f"[LogManager@setupLogging] Error configuring logging: {ERR_01}")
            raise SystemExit(-1)

    @classmethod
    def getLogger(cls) -> Logger:
        """
        Returns the configured logger instance.

        :return: The logger instance.
        """

        return cls.logger
