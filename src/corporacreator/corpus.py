import os
import logging

import corporacreator.preprocessors as preprocessors

import pandas as pd


_logger = logging.getLogger(__name__)


class Corpus:
    def __init__(self, args, locale, corpus_data):
        self.args = args
        self.locale = locale
        self.corpus_data = corpus_data

    def create(self):
        _logger.debug("Creating %s corpus..." % self.locale)
        self._pre_process_corpus_data()
        self._partition_corpus_data()
        self._post_process_valid_data()
        # Do it here....
        _logger.debug("Created %s corpora." % self.locale)

    def _pre_process_corpus_data(self):
        self.corpus_data["user_id"] = self.corpus_data["path"].str.split(
            "/", expand=True
        )[0] # TODO: Remove this line when the Gregor modifies the csv output to include user_id
        preprocessor = getattr(preprocessors, self.locale.replace("-","")) # Get locale specific preprocessor
        self.corpus_data["sentence"] = self.corpus_data["sentence"].apply(func=preprocessor)

    def _partition_corpus_data(self):
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

    def _post_process_valid_data(self):
        speaker_counts = self.valid["user_id"].value_counts()
        speaker_counts = speaker_counts.to_frame().reset_index()
        speaker_counts.columns = ["user_id", "user_sentence_count"]
        self.valid = self.valid.join(speaker_counts.set_index("user_id"), on="user_id")

    def save(self, directory):
        directory = os.path.join(directory, self.locale)
        if not os.path.exists(directory):
            os.mkdir(directory)
        other_path = os.path.join(directory, "other.tsv")
        invalid_path = os.path.join(directory, "invalid.tsv")
        valid_path = os.path.join(directory, "valid.tsv")

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
        self.valid.to_csv(
            valid_path,
            sep="\t",
            header=True,
            index=False,
            encoding="utf-8",
            escapechar='"',
        )
        # Do it here....
        _logger.debug("Saved %s corpora." % self.locale)
