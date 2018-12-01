import logging

import pandas as pd


_logger = logging.getLogger(__name__)

class Corpus():
    def __init__(self, locale, corpusdata):
        self.locale = locale
        self.corpusdata = corpusdata

    def create(self):
        _logger.debug("Creating %s corpus..." % self.locale)
        # Do it here....
        _logger.debug("Created %s corpora." % self.locale)

    def save(self):
        _logger.debug("Saving %s corpora..." % self.locale)
        # Do it here....
        _logger.debug("Saved %s corpora." % self.locale)
