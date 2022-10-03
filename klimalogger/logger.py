import logging


def create_console_handler():
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    return console_handler


def get_logger_name(clazz):
    return "{}.{}".format(clazz.__module__, clazz.__name__)
