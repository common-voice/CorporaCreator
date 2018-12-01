import sys
import logging

import pandas as pd


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
        corporadata = pd.read_csv(self.args.tsvfilename,
            sep="\t",
            parse_dates=False,
            engine="python",
            encoding="utf-8",
            error_bad_lines=False)
        _logger.debug("Parsed tsv file.")
        return corporadata

    def save(self):
        _logger.debug("Saving corpora...")
        # Do it here....
        _logger.debug("Saved corpora.")
