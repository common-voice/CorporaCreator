import os
import logging

import pandas as pd

from corporacreator import Corpus


_logger = logging.getLogger(__name__)


class Corpora:
    def __init__(self, args):
        self.args = args
        self.corpora = []

    def create(self):
        _logger.debug("Creating corpora...")
        corpora_data = self._parse_tsv()
        for locale in corpora_data.locale.unique():
            _logger.debug("Selecting %s corpus data..." % locale)
            corpus_data = corpora_data.loc[
                lambda df: df.locale == locale,
                [
                    "path",
                    "sentence",
                    "up_votes",
                    "down_votes",
                    "age",
                    "gender",
                    "accent",
                ],
            ]
            _logger.debug("Selected %s corpus data." % locale)
            _logger.debug("Creating %s corpus..." % locale)
            corpus = Corpus(locale, corpus_data)
            corpus.create()
            _logger.debug("Created %s corpus." % locale)
            self.corpora.append(corpus)
        _logger.debug("Created corpora.")

    def _parse_tsv(self):
        _logger.debug("Parsing tsv file...")
        corpora_data = pd.read_csv(
            self.args.tsv_filename,
            sep="\t",
            parse_dates=False,
            engine="python",
            encoding="utf-8",
            error_bad_lines=False,
        )
        _logger.debug("Parsed tsv file.")
        return corpora_data

    def save(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        _logger.debug("Saving corpora...")
        for corpus in self.corpora:
            _logger.debug("Saving %s corpus..." % corpus.locale)
            corpus.save(directory)
            _logger.debug("Saved %s corpus." % corpus.locale)
        _logger.debug("Saved corpora.")
