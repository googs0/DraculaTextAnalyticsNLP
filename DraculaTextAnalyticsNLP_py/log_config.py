import logging
import logging.config
from colorama import init, Fore, Style
import sys

init()

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Style.BRIGHT + Fore.RED,
    }

    RESET = Style.RESET_ALL

    def format(self, record):
        log_message = super().format(record)
        log_level = record.levelname

        # Add color to log messages based on log level
        if log_level in self.COLORS:
            log_message = f"{self.COLORS[log_level]}{log_message}{self.RESET}"

        sys.stdout.flush()

        return log_message


def setup_logging():
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the StreamHandler to the root logger
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().setLevel(logging.DEBUG)
