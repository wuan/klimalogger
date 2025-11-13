import sys


def create_logger(name: str):
    if sys.implementation.name == "circuitpython":
        import adafruit_logging

        return adafruit_logging.Logger(__name__)
    else:
        import logging

        return logging.getLogger(__name__)


def create_console_handler():
    import logging

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    return console_handler


def get_logger_name(clazz):
    return f"{clazz.__module__}.{clazz.__name__}"
