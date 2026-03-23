import csv
import logging
import os

import pandas as pd  # type: ignore
import swifter  # type: ignore # noqa: F401 -- side-effect import, patches pandas with .swifter accessor

import corporacreator
import corporacreator.preprocessors as preprocessors
from corporacreator.resources import log_resources

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
        rows = len(self.corpus_data)
        _logger.debug("Creating %s corpus (%d rows)..." % (self.locale, rows))
        log_resources("before preprocess %s" % self.locale, "%d rows" % rows)
        self._pre_process_corpus_data()
        log_resources("after preprocess %s" % self.locale)
        self._partition_corpus_data()
        log_resources("after partition %s" % self.locale,
                      "valid=%d invalid=%d other=%d" % (
                          len(self.validated), len(self.invalidated), len(self.other)))
        del self.corpus_data
        self._post_process_valid_data()
        log_resources("after split %s" % self.locale,
                      "train=%d dev=%d test=%d" % (
                          len(self.train), len(self.dev), len(self.test)))
        _logger.debug("Created %s corpora." % self.locale)

    def _pre_process_corpus_data(self):
        self.corpus_data[["sentence", "up_votes", "down_votes"]] = self.corpus_data[
            ["client_id", "sentence", "up_votes", "down_votes"]
        ].swifter.apply(func=lambda arg: self._preprocessor_wrapper(*arg), axis=1)

    def _preprocessor_default(self, client_id, sentence):
        return sentence

    def _preprocessor_wrapper(self, client_id, sentence, up_votes, down_votes):
        preprocessor = getattr(
            preprocessors, self.locale.replace("-", ""), self._preprocessor_default
        )  # Get locale specific preprocessor
        sentence = preprocessor(client_id, sentence)
        if sentence is None or not sentence.strip():
            up_votes = 0
            down_votes = 2
        return pd.Series([sentence, up_votes, down_votes])

    def _partition_corpus_data(self):
        # If there are < 2 votes, or 2 opposing votes
        # there is not enough information to make a determination
        self.other = self.corpus_data.loc[
            lambda df: (df.up_votes + df.down_votes <= 1)
            | ((df.up_votes == 1) & (df.down_votes == 1)), :
        ]
        # If there are 2+ votes, and up_votes > down_votes, clip is valid
        self.validated = self.corpus_data.loc[
            lambda df: (df.up_votes + df.down_votes > 1)
            & (df.up_votes > df.down_votes),
            :,
        ]
        # If there are 2+ votes, and down_votes > up_votes, clip is invalid
        # If there are 3+ votes, and up_votes == down_votes, opinions
        # are diverging too much to be relied upon, and clip is invalid
        self.invalidated = self.corpus_data.loc[
            lambda df: ((df.up_votes + df.down_votes > 1)
                & (df.up_votes < df.down_votes))
            | ((df.up_votes == df.down_votes)
                & (df.up_votes + df.down_votes > 2)),
            :,
        ]

    def _post_process_valid_data(self):
        # Remove duplicate sentences while maintaining maximal user diversity at the frame's start (TODO: Make addition of user_sentence_count cleaner)
        speaker_counts = self.validated["client_id"].value_counts()
        speaker_counts = speaker_counts.to_frame().reset_index()
        speaker_counts.columns = ["client_id", "user_sentence_count"]
        self.validated = self.validated.join(
            speaker_counts.set_index("client_id"), on="client_id"
        )
        self.validated = self.validated.sort_values(["user_sentence_count", "client_id"])
        validated = self.validated.groupby("sentence").head(self.args.duplicate_sentence_count)

        validated = validated.sort_values(["user_sentence_count", "client_id"], ascending=False)
        validated = validated.drop(columns="user_sentence_count")
        self.validated = self.validated.drop(columns="user_sentence_count")


        train = pd.DataFrame(columns=validated.columns)
        dev = pd.DataFrame(columns=validated.columns)
        test = pd.DataFrame(columns=validated.columns)

        train_size = dev_size = test_size = 0

        if (len(validated) > 0):
            # Determine train, dev, and test sizes
            train_size, dev_size, test_size = self._calculate_data_set_sizes(len(validated))
            # Split into train, dev, and test datasets
            continous_client_index, uniques = pd.factorize(validated["client_id"])
            validated["continous_client_index"] = continous_client_index

            # Pre-partition by speaker once (O(n)) instead of scanning per iteration (O(n²))
            groups = {k: v for k, v in validated.groupby("continous_client_index", sort=False)}

            train_parts, dev_parts, test_parts = [], [], []
            test_count = dev_count = 0

            for i in range(max(continous_client_index), -1, -1):
                speaker_data = groups[i]
                n = len(speaker_data)
                if test_count + n <= test_size:
                    test_parts.append(speaker_data)
                    test_count += n
                elif dev_count + n <= dev_size:
                    dev_parts.append(speaker_data)
                    dev_count += n
                else:
                    train_parts.append(speaker_data)

            train = pd.concat(train_parts, sort=False) if train_parts else pd.DataFrame(columns=validated.columns)
            dev   = pd.concat(dev_parts, sort=False)   if dev_parts   else pd.DataFrame(columns=validated.columns)
            test  = pd.concat(test_parts, sort=False)   if test_parts  else pd.DataFrame(columns=validated.columns)

        self.train = train.drop(columns="continous_client_index", errors="ignore")
        self.dev = dev.drop(columns="continous_client_index", errors="ignore")
        self.test = test[:train_size].drop(columns="continous_client_index", errors="ignore")

    def _calculate_data_set_sizes(self, total_size):
        # Find maximum size for the training data set in accord with sample theory
        train_size = total_size
        dev_size = 0
        test_size = 0
        for train_size in range(total_size, 0, -1):
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
        datasets = ["other", "invalidated", "validated", "train", "dev", "test"]

        _logger.debug("Saving %s corpora..." % self.locale)
        for dataset in datasets:
            self._save(directory, dataset)
        _logger.debug("Saved %s corpora." % self.locale)

    def _save(self, directory, dataset):
        path = os.path.join(directory, dataset + ".tsv")

        dataframe = getattr(self, dataset)
        dataframe.to_csv(
            path, sep="\t", header=True, index=False, encoding="utf-8", escapechar='\\', quoting=csv.QUOTE_NONE
        )