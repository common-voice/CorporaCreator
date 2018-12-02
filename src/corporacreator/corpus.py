import os
import logging

import pandas as pd


_logger = logging.getLogger(__name__)


class Corpus:
    def __init__(self, locale, corpus_data):
        self.locale = locale
        self.corpus_data = corpus_data

    def create(self):
        _logger.debug("Creating %s corpus..." % self.locale)
        self.other = self.corpus_data.loc[
            lambda df: (df.up_votes + df.down_votes) <= 1, :
        ]
        self.valid = self.corpus_data.loc[
            lambda df: (df.up_votes + df.down_votes > 1)
            & (df.up_votes > df.down_votes),
            :,
        ]
        self.invalid = self.corpus_data.loc[
            lambda df: (df.up_votes + df.down_votes > 1)
            & (df.up_votes <= df.down_votes),
            :,
        ]
        # Do it here....
        _logger.debug("Created %s corpora." % self.locale)

    def save(self, directory):
        directory = os.path.join(directory, self.locale)
        if not os.path.exists(directory):
            os.mkdir(directory)
        other_path = os.path.join(directory, "other.tsv")
        invalid_path = os.path.join(directory, "invalid.tsv")

        _logger.debug("Saving %s corpora..." % self.locale)
        self.other.to_csv(
            other_path,
            sep="\t",
            header=True,
            index=False,
            encoding="utf-8",
            escapechar='"',
        )
        self.invalid.to_csv(
            invalid_path,
            sep="\t",
            header=True,
            index=False,
            encoding="utf-8",
            escapechar='"',
        )
        # Do it here....
        _logger.debug("Saved %s corpora." % self.locale)
