import os
import csv
import logging

import pandas as pd

from corporacreator import Corpus


_logger = logging.getLogger(__name__)


class Corpora:
    def __init__(self, args):
        self.args = args
        self.corpora = []

    def create(self):
        _logger.info("Creating corpora...")
        corpora_data = self._parse_tsv()
        for locale in corpora_data.locale.unique():
            _logger.info("Selecting %s corpus data..." % locale)
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
            _logger.info("Selected %s corpus data." % locale)
            _logger.info("Creating %s corpus..." % locale)
            corpus = Corpus(locale, corpus_data)
            corpus.create()
            _logger.info("Created %s corpus." % locale)
            self.corpora.append(corpus)
        _logger.info("Created corpora.")

    def _parse_tsv(self):
        _logger.info("Parsing tsv file...")
        corpora_data = pd.read_csv(
            self.args.tsv_filename,
            sep="\t",
            parse_dates=False,
            engine="python",
            encoding="utf-8",
            error_bad_lines=False,
            quotechar='"',
            quoting=csv.QUOTE_NONE,
        )
        _logger.info("Parsed %d lines tsv file." % len(corpora_data))
        return corpora_data

    def save(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        _logger.info("Saving corpora...")
        for corpus in self.corpora:
            _logger.info("Saving %s corpus..." % corpus.locale)
            corpus.save(directory)
            _logger.info("Saved %s corpus." % corpus.locale)
        _logger.info("Saved corpora.")
