import sys
import logging

__license__ = "mpl"
__author__ = "kdavis-mozilla"
__copyright__ = "kdavis-mozilla"
_logger = logging.getLogger(__name__)


class Creator():
    def __init__(self, args):
        self.args = args

    def create(self):
        _logger.info("Creator creating corpora...")
        # Do it here....
        _logger.info("Creator finished creating corpora...")
