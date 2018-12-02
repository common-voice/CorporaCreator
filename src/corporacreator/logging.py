import sys
import logging


def setup_logging(level):
    """Setup basic logging

    Args:
      level (int): minimum log level for emitting messages
    """
    format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=level, stream=sys.stdout, format=format, datefmt="%Y-%m-%d %H:%M:%S")
