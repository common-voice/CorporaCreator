import os
import csv
import logging

import swifter
import pandas as pd

from corporacreator import Corpus
from corporacreator.preprocessors import common
import argparse

_logger = logging.getLogger(__name__)


def common_wrapper(sentence, up_votes, down_votes):
    sentence = common(sentence)
    if None == sentence or not sentence.strip():
        up_votes = 0
        down_votes = 2
    return pd.Series([sentence, up_votes, down_votes])


class Corpora:
    """Corpora representing all Common Voice datasets.

    Args:
      args ([str]): Command line parameters as list of strings

    Attributes:
        args ([str]): command line parameters as list of strings
        corpora ([:class:`corporacreator.Corpus`]): List of :class:`corporacreator.Corpus` instances
    """

    def __init__(self, args):
        self.args = args
        self.corpora = []

    def create(self):
        """Creates a :class:`corporacreator.Corpus` for each locale.
        """
        _logger.info("Creating corpora...")
        corpora_data = self._parse_tsv()
        corpora_data[["sentence", "up_votes", "down_votes"]] = corpora_data[
            ["sentence", "up_votes", "down_votes"]
        ].swifter.apply(func=lambda arg: common_wrapper(*arg), axis=1)
        if self.args.langs:
            # check if all languages provided at command line are actually
            # in the clips.tsv file, if not, throw error
            if self.args.langs.issubset(corpora_data.locale.unique()):
                locales = self.args.langs
            else:
                raise argparse.ArgumentTypeError("ERROR: You have requested languages which do not exist in clips.tsv")
        else:
            locales = corpora_data.locale.unique()
            
        for locale in locales:
            _logger.info("Selecting %s corpus data..." % locale)
            corpus_data = corpora_data.loc[
                lambda df: df.locale == locale,
                [
                    "client_id",
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
            corpus = Corpus(self.args, locale, corpus_data)
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
        """Saves this :class:`corporacreator.Corpora` in `directory`.

        Args:
          directory (str): Directory into which this `corporacreator.Corpora` is saved.
        """
        if not os.path.exists(directory):
            os.mkdir(directory)
        _logger.info("Saving corpora...")
        for corpus in self.corpora:
            _logger.info("Saving %s corpus..." % corpus.locale)
            corpus.save(directory)
            _logger.info("Saved %s corpus." % corpus.locale)
        _logger.info("Saved corpora.")
