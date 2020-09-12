try:
    import coloredlogs
except ImportError:
    coloredlogs = False
    pass

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

if coloredlogs:
    coloredlogs.install(level="INFO", logger=logger)


def set_logger_level(level):
    logger.setLevel(level)

    if coloredlogs:
        coloredlogs.install(
            fmt="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
            datefmt="%H:%M:%S",
            level=level,
            logger=logger,
        )


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


__all__ = ["debug", "info", "warning", "error", "set_logger_level", "logging"]
