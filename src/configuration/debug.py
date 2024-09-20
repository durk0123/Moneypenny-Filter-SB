import logging
from src.utilities.console import TerminalColors, ColoredFormatter

def setup_logging() -> logging.Logger:
    """
    Sets up the logging configuration for the bot with color formatting.
    Configures the logger to use a custom formatter for colored output in the console.

    :return: The configured logger for Discord bot logging.
    """
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)  # Adjust the logging level as needed

    # Remove all existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a console handler and set its custom colored formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(message)s'))  # Define custom format if necessary
    logger.addHandler(console_handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    return logger
