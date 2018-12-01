import sys
import logging

from numpy import genfromtxt


_logger = logging.getLogger(__name__)

class Corpora():
    def __init__(self, args):
        self.args = args

    def create(self):
        _logger.debug("Creating corpora...")
        corporadata = self._parse_tsv()
        # Do it here....
        _logger.debug("Created corpora.")

    def _parse_tsv(self):
        _logger.debug("Parsing tsv file...")
        corporadata = genfromtxt(self.args.tsvfilename,
            delimiter="\t",
            dtype=None,
            skip_header=1,
            encoding="utf8")
        _logger.debug("Parsed tsv file.")
        return corporadata

    def save(self):
        _logger.debug("Saving corpora...")
        # Do it here....
        _logger.debug("Saved corpora.")
