import sys
import logging


_logger = logging.getLogger(__name__)

class Corpora():
    def __init__(self, args):
        self.args = args

    def create(self):
        _logger.debug("Creating corpora...")
        # Do it here....
        _logger.debug("Finished creating corpora.")

    def save(self):
        _logger.debug("Saving corpora...")
        # Do it here....
        _logger.debug("Finished saving corpora.")
