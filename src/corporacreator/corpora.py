import logging

import pandas as pd

from corporacreator import Corpus


_logger = logging.getLogger(__name__)

class Corpora():
    def __init__(self, args):
        self.args = args
        self.corpora = []

    def create(self):
        _logger.debug("Creating corpora...")
        corporadata = self._parse_tsv()
        for locale in corporadata.locale.unique():
            _logger.debug("Selecting %s corpus data..." % locale)
            corpusdata = corporadata.loc[lambda df: df.locale == locale, corporadata.columns != locale]
            _logger.debug("Selected %s corpus data." % locale)
            _logger.debug("Creating %s corpus..." % locale)
            corpus = Corpus(locale, corpusdata)
            corpus.create()
            _logger.debug("Created %s corpus." % locale)
            self.corpora.append(corpus)
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
        for corpus in self.corpora:
            _logger.debug("Saving %s corpus..." % corpus.locale)
            corpus.save()
            _logger.debug("Saved %s corpus." % corpus.locale)
        _logger.debug("Saved corpora.")
