# System imports
import os
import logging
from datetime import datetime

def clear_console() -> None:
    """
    Clears the console screen.

    Detects the operating system and executes the appropriate command 
    to clear the console. It uses 'cls' for Windows and 'clear' for macOS and Linux.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def timestamp() -> str:
    """
    Returns the current time formatted as a string in [HH:MM:SS AM/PM] format.

    Useful for timestamping logs or other time-sensitive operations.
    
    :return: A string representing the current time in [HH:MM:SS AM/PM] format.
    """
    return datetime.now().strftime("%I:%M:%S %p")

class TerminalColors:
    """
    A class to define ANSI color codes for terminal output, 
    which can be used to colorize text output in the console.
    """
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds color to log levels and enhances the output format
    for better readability in the terminal.
    """

    # Define colors for different log levels
    LEVEL_COLORS = {
        logging.DEBUG: TerminalColors.GRAY,
        logging.INFO: TerminalColors.GREEN,
        logging.WARNING: TerminalColors.YELLOW,
        logging.ERROR: TerminalColors.RED,
        logging.CRITICAL: TerminalColors.MAGENTA
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record with color, a timestamp, and details like level and logger name.

        :param record: The log record to format.
        :return: A formatted string with colorized level, timestamp, and log message.
        """
        log_color = self.LEVEL_COLORS.get(record.levelno, TerminalColors.RESET)
        reset_color = TerminalColors.RESET

        # Format the time using the timestamp helper
        formatted_time = timestamp()

        # Create the formatted log level, logger name, and message
        log_level = f"{log_color}{record.levelname:<8}{reset_color}"
        logger_name = f"{TerminalColors.CYAN}{record.name}{reset_color}"

        # Build the formatted log message
        formatted_message = f"[{TerminalColors.GRAY}{formatted_time}{reset_color}] {log_level} [{logger_name}] {record.getMessage()}"

        # Add exception info if present, formatted in red for visibility
        if record.exc_info:
            formatted_message += f"\n{TerminalColors.RED}{self.formatException(record.exc_info)}{reset_color}"

        return formatted_message