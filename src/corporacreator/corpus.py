import logging
import os

import polars as pl

import corporacreator
import corporacreator.preprocessors as preprocessors
from corporacreator.resources import log_resources

_logger = logging.getLogger(__name__)


class Corpus:
    """Corpus representing a Common Voice dataset for a given locale.

    Args:
      args ([str]): Command line parameters as list of strings
      locale (str): Locale this :class:`corporacreator.Corpus` represents
      corpus_data (:class:`polars.DataFrame`): DataFrame containing the corpus data

    Attributes:
        args ([str]): Command line parameters as list of strings
        locale (str): Locale of this :class:`corporacreator.Corpus`
        corpus_data (:class:`polars.DataFrame`): DataFrame containing the corpus data
    """

    def __init__(self, args, locale, corpus_data):
        self.args = args
        self.locale = locale
        self.corpus_data = corpus_data

    def create(self):
        """Creates a :class:`corporacreator.Corpus` for `self.locale`."""
        rows = len(self.corpus_data)
        _logger.debug("Creating %s corpus (%d rows)..." % (self.locale, rows))
        log_resources("before preprocess %s" % self.locale, "%d rows" % rows)
        self._preprocess_locale()
        log_resources("after preprocess %s" % self.locale)
        self._partition()
        log_resources(
            "after partition %s" % self.locale,
            "valid=%d invalid=%d other=%d"
            % (len(self.validated), len(self.invalidated), len(self.other)),
        )
        del self.corpus_data
        self._post_process_validated()
        log_resources(
            "after split %s" % self.locale,
            "train=%d dev=%d test=%d"
            % (len(self.train), len(self.dev), len(self.test)),
        )
        _logger.debug("Created %s corpus." % self.locale)

    # ------------------------------------------------------------------
    # Locale-specific preprocessing
    # ------------------------------------------------------------------

    def _preprocess_locale(self):
        """Apply locale-specific preprocessor -- skipped if none exists."""
        locale_key = self.locale.replace("-", "")
        proc = getattr(preprocessors, locale_key, None)
        if proc is None:
            return  # no preprocessor for this locale (e.g. ps, en) -- skip

        _logger.debug("Applying %s locale preprocessor..." % self.locale)

        # Build a struct of the columns the preprocessor needs, then
        # map_elements to apply the locale-specific function per row.
        new_sentence = (
            pl.struct(["client_id", "sentence"])
            .map_elements(
                lambda row: proc(row["client_id"], row["sentence"]),
                return_dtype=pl.String,
            )
        )

        is_invalid = new_sentence.is_null() | (
            new_sentence.str.strip_chars().str.len_chars().eq(0)
        )

        self.corpus_data = self.corpus_data.with_columns([
            new_sentence.alias("sentence"),
            pl.when(is_invalid)
            .then(0)
            .otherwise(pl.col("up_votes"))
            .alias("up_votes"),
            pl.when(is_invalid)
            .then(2)
            .otherwise(pl.col("down_votes"))
            .alias("down_votes"),
        ])

    # ------------------------------------------------------------------
    # Partition
    # ------------------------------------------------------------------

    def _partition(self):
        df = self.corpus_data
        vote_sum = pl.col("up_votes") + pl.col("down_votes")

        # If there are < 2 votes, or 2 opposing votes
        # there is not enough information to make a determination
        self.other = df.filter(
            (vote_sum <= 1)
            | ((pl.col("up_votes") == 1) & (pl.col("down_votes") == 1))
        )
        # If there are 2+ votes, and up_votes > down_votes, clip is valid
        self.validated = df.filter(
            (vote_sum > 1) & (pl.col("up_votes") > pl.col("down_votes"))
        )
        # If there are 2+ votes, and down_votes > up_votes, clip is invalid
        # If there are 3+ votes, and up_votes == down_votes, clip is invalid
        self.invalidated = df.filter(
            ((vote_sum > 1) & (pl.col("up_votes") < pl.col("down_votes")))
            | (
                (pl.col("up_votes") == pl.col("down_votes"))
                & (vote_sum > 2)
            )
        )

    # ------------------------------------------------------------------
    # Validated post-processing: dedup + split
    # ------------------------------------------------------------------

    def _post_process_validated(self):
        validated = self.validated

        if len(validated) == 0:
            self.train = self.dev = self.test = validated
            return

        # --- Speaker clip counts ---
        speaker_counts = (
            validated
            .group_by("client_id")
            .agg(pl.len().alias("user_sentence_count"))
        )
        validated = (
            validated
            .join(speaker_counts, on="client_id")
            .sort(["user_sentence_count", "client_id"])
        )

        # Store validated with user_sentence_count dropped (matches v1 output)
        self.validated = validated.drop("user_sentence_count")

        # --- Sentence deduplication ---
        # Keep first N occurrences per sentence (those with lowest
        # user_sentence_count = most diverse speakers), matching v1's
        # groupby("sentence").head(n)
        deduped = (
            validated
            .with_row_index("_row_idx")
            .with_columns(
                pl.col("_row_idx")
                .rank("ordinal")
                .over("sentence")
                .alias("_sentence_rank")
            )
            .filter(
                pl.col("_sentence_rank") <= self.args.duplicate_sentence_count
            )
            .drop(["_row_idx", "_sentence_rank"])
        )

        # Sort descending (speakers with most clips first = lowest factorize
        # index in v1) then prepare for split
        deduped = deduped.sort(
            ["user_sentence_count", "client_id"], descending=True
        )

        train_size, dev_size, test_size = self._calculate_split_sizes(
            len(deduped)
        )

        # --- Speaker split (exact v1 logic, O(n) via speaker-level loop) ---
        # Get unique speakers in order of first appearance (most clips first
        # in descending-sorted deduped), then reverse to match v1's
        # range(max(continous_client_index), -1, -1) which processes
        # speakers with fewest clips first.
        speaker_order = (
            deduped
            .select("client_id")
            .unique(maintain_order=True)
            .reverse()
        )

        # Get clip count per speaker
        speaker_clip_counts = (
            deduped
            .group_by("client_id")
            .agg(pl.len().alias("_n_clips"))
        )
        speaker_order = speaker_order.join(
            speaker_clip_counts, on="client_id", how="left", maintain_order="left"
        )

        # Assign split labels with exact v1 budget logic
        test_used = dev_used = 0
        labels = []
        for n in speaker_order["_n_clips"].to_list():
            if test_used + n <= test_size:
                labels.append("test")
                test_used += n
            elif dev_used + n <= dev_size:
                labels.append("dev")
                dev_used += n
            else:
                labels.append("train")

        speaker_order = speaker_order.with_columns(
            pl.Series("_split", labels)
        )

        # Join split labels back -- single O(n) join, no concat loop
        result = deduped.join(
            speaker_order.select(["client_id", "_split"]),
            on="client_id",
        ).drop("user_sentence_count")

        self.train = (
            result.filter(pl.col("_split") == "train").drop("_split")
        )
        self.dev = (
            result.filter(pl.col("_split") == "dev").drop("_split")
        )
        self.test = (
            result.filter(pl.col("_split") == "test")
            .drop("_split")
            .head(test_size)
        )

    def _calculate_split_sizes(self, total_size):
        """Binary search for max train_size where
        2 * sample_size(train_size) + train_size <= total_size.

        f(t) = 2*sample_size(t) + t is strictly monotonically increasing,
        so binary search applies. O(log N) = ~23 iterations for 5M clips
        vs ~33K iterations in v1.
        """
        if total_size == 0:
            return 0, 0, 0

        lo, hi = 0, total_size
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if 2 * int(corporacreator.sample_size(mid)) + mid <= total_size:
                lo = mid
            else:
                hi = mid - 1
        train_size = lo
        sample = int(corporacreator.sample_size(train_size))
        return train_size, sample, sample

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, directory):
        """Saves this :class:`corporacreator.Corpus` in `directory`.

        Args:
          directory (str): Directory into which this `corporacreator.Corpus` is saved.
        """
        directory = os.path.join(directory, self.locale)
        if not os.path.exists(directory):
            os.mkdir(directory)
        datasets = ["other", "invalidated", "validated", "train", "dev", "test"]

        _logger.debug("Saving %s corpus..." % self.locale)
        for dataset in datasets:
            self._save(directory, dataset)
        _logger.debug("Saved %s corpus." % self.locale)

    def _save(self, directory, dataset):
        path = os.path.join(directory, dataset + ".tsv")
        df: pl.DataFrame = getattr(self, dataset)
        df.write_csv(path, separator="\t", quote_style="never")
