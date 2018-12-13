import os
import logging

import corporacreator
import corporacreator.preprocessors as preprocessors

import pandas as pd


_logger = logging.getLogger(__name__)

class Corpus:
    """Corpus representing a Common Voice datasets for a given locale.

    Args:
      args ([str]): Command line parameters as list of strings
      locale (str): Locale this :class:`corporacreator.Corpus` represents
      corpus_data (:class:`pandas.DataFrame`): `pandas.DataFrame` Containing the corpus data

    Attributes:
        args ([str]): Command line parameters as list of strings
        locale (str): Locale of this :class:`corporacreator.Corpus` 
        corpus_data (:class:`pandas.DataFrame`): `pandas.DataFrame` Containing the corpus data
    """
    def __init__(self, args, locale, corpus_data):
        self.args = args
        self.locale = locale
        self.corpus_data = corpus_data

    def create(self):
        """Creates a :class:`corporacreator.Corpus` for `self.locale`.
        """
        _logger.debug("Creating %s corpus..." % self.locale)
        self._pre_process_corpus_data()
        self._partition_corpus_data()
        self._post_process_valid_data()
        _logger.debug("Created %s corpora." % self.locale)

    def _pre_process_corpus_data(self):
        preprocessor = getattr(preprocessors, self.locale.replace("-","")) # Get locale specific preprocessor
        self.corpus_data["sentence"] = self.corpus_data[["client_id", "sentence"]].apply(func=lambda arg: preprocessor(*arg), axis=1)

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
        # Remove duplicate sentences while maintaining maximal user diversity at the frame's start (TODO: Make addition of user_sentence_count cleaner)
        speaker_counts = self.valid["client_id"].value_counts()
        speaker_counts = speaker_counts.to_frame().reset_index()
        speaker_counts.columns = ["client_id", "user_sentence_count"]
        self.valid = self.valid.join(speaker_counts.set_index("client_id"), on="client_id")
        self.valid = self.valid.sort_values(["user_sentence_count", "client_id"])
        valid = self.valid.groupby("sentence").head(self.args.duplicate_sentence_count)
        valid = valid.sort_values(["user_sentence_count", "client_id"], ascending=False)
        valid = valid.drop(columns="user_sentence_count")
        self.valid = self.valid.drop(columns="user_sentence_count")
        # Determine train, dev, and test sizes
        train_size, dev_size, test_size = self._calculate_data_set_sizes(len(valid))
        # Split into train, dev, and test datasets
        self.train = valid.iloc[0:train_size]
        self.dev = valid.iloc[train_size:train_size + dev_size]
        self.test = valid.iloc[train_size + dev_size:train_size + dev_size + test_size]
        # TODO: Make sure users are in train, dev, xor test

    def _calculate_data_set_sizes(self, total_size):
        # Find maximum size for the training data set in accord with sample theory
        for train_size  in range(total_size, 0, -1):
            calculated_sample_size = int(corporacreator.sample_size(train_size))
            if 2 * calculated_sample_size + train_size <= total_size:
                dev_size = calculated_sample_size
                test_size = calculated_sample_size
                break
        return train_size, dev_size, test_size

    def save(self, directory):
        """Saves this :class:`corporacreator.Corpus` in `directory`.

        Args:
          directory (str): Directory into which this `corporacreator.Corpus` is saved.
        """
        directory = os.path.join(directory, self.locale)
        if not os.path.exists(directory):
            os.mkdir(directory)
        datasets = ["other", "invalid", "valid", "train", "dev", "test"]

        _logger.debug("Saving %s corpora..." % self.locale)
        for dataset in datasets:
            self._save(directory, dataset)
        _logger.debug("Saved %s corpora." % self.locale)

    def _save(self, directory, dataset):
        path = os.path.join(directory, dataset + ".tsv")
        dataframe = getattr(self, dataset)
        dataframe.to_csv(
            path,
            sep="\t",
            header=True,
            index=False,
            encoding="utf-8",
            escapechar='"',
        )
