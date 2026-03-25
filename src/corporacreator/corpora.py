import argparse
import html
import logging
import os
import re
from urllib.parse import unquote

import polars as pl

from corporacreator import Corpus
from corporacreator.resources import log_resources

_logger = logging.getLogger(__name__)

# Compiled regex for HTML tag stripping (used in _clean_sentence)
_RE_HTML_TAGS = re.compile(r"<[^>]+>")


def _clean_sentence(sentence: str) -> str:
    """Clean a single sentence: URL decode, strip HTML, strip disallowed unicode.

    This is called via map_elements for the steps that require Python-level
    processing. Whitespace normalization and validity checks are done
    vectorized in Polars afterward.
    """
    sentence = str(sentence)
    # URL decode
    if "%" in sentence:
        sentence = unquote(sentence)
    # Strip HTML tags via regex
    sentence = _RE_HTML_TAGS.sub("", sentence)
    # Convert HTML entities (&amp; -> &, etc.)
    if "&" in sentence:
        sentence = html.unescape(sentence)
    return sentence


# Columns expected in clips.tsv (used for column pushdown on read)
COLUMNS = [
    "client_id",
    "path",
    "sentence_id",
    "sentence",
    "sentence_domain",
    "up_votes",
    "down_votes",
    "age",
    "gender",
    "accents",
    "variant",
    "locale",
    "segment",
]

SCHEMA_OVERRIDES = {
    "up_votes": pl.Int32,
    "down_votes": pl.Int32,
}


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
        """Creates a :class:`corporacreator.Corpus` for each locale."""
        _logger.info("Creating corpora...")
        df = self._parse_tsv()
        log_resources("before preprocess_common")
        df = self._preprocess_common(df)
        log_resources("after preprocess_common")

        if self.args.langs:
            available = set(df["locale"].unique().to_list())
            if not set(self.args.langs).issubset(available):
                raise argparse.ArgumentTypeError(
                    "ERROR: You have requested languages which do not exist in clips.tsv"
                )
            locales = self.args.langs
        else:
            locales = df["locale"].unique().to_list()

        for locale in locales:
            _logger.info("Selecting %s corpus data..." % locale)
            locale_df = df.filter(pl.col("locale") == locale)
            _logger.info("Selected %s corpus data." % locale)

            _logger.info("Creating %s corpus..." % locale)
            corpus = Corpus(self.args, locale, locale_df)
            corpus.create()
            _logger.info("Created %s corpus." % locale)
            self.corpora.append(corpus)

        del df

        log_resources("after all corpora created")
        _logger.info("Created corpora.")

    def _parse_tsv(self) -> pl.DataFrame:
        log_resources("before read_csv")
        _logger.info("Parsing tsv file...")
        df = (
            pl.scan_csv(
                self.args.tsv_filename,
                separator="\t",
                encoding="utf8",
                schema_overrides=SCHEMA_OVERRIDES,
                ignore_errors=True,
                quote_char=None,
            )
            .select([c for c in COLUMNS])
            .collect()
        )
        # Warn about silently skipped rows (Polars ignore_errors has no
        # built-in warning mode, unlike pandas on_bad_lines="warn")
        file_lines = self._count_file_lines(self.args.tsv_filename) - 1  # minus header
        if len(df) < file_lines:
            _logger.warning(
                "Skipped %d malformed rows during TSV parsing", file_lines - len(df)
            )
        _logger.info("Parsed %d lines tsv file." % len(df))
        if _logger.isEnabledFor(logging.DEBUG):
            mem_mb = df.estimated_size("mb")
            log_resources("after read_csv", "%d rows, DataFrame=%.0fMB" % (len(df), mem_mb))
        return df

    @staticmethod
    def _count_file_lines(path: str) -> int:
        """Count newlines in a file using buffered binary read."""
        count = 0
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                count += chunk.count(b"\n")
        return count

    def _preprocess_common(self, df: pl.DataFrame) -> pl.DataFrame:
        """Vectorized equivalent of the old swifter common_wrapper apply.

        Pipeline:
          1. URL decode + HTML strip + entity decode  (map_elements -- Python)
          2. Strip disallowed unicode categories       (vectorized Polars regex)
          3. Normalize whitespace                      (vectorized Polars str ops)
          4. Validity: digits / empty                  (vectorized boolean masks)
        """
        s = df["sentence"].cast(pl.String)

        # 1. Python-level cleaning: URL decode, HTML tags, HTML entities
        s = s.map_elements(_clean_sentence, return_dtype=pl.String)

        # 2. Strip disallowed unicode -- FULLY VECTORIZED via Polars/Rust regex
        #    Allowed categories (matches v1 _strip_string exactly):
        #      Letters (L), Numbers (N), Marks (M), Punctuation (P),
        #      Symbols (S), Space Separators (Zs)
        s = s.str.replace_all(r"[^\p{L}\p{N}\p{M}\p{P}\p{S}\p{Zs}]", "")

        # 3. Normalize whitespace -- vectorized
        s = s.str.replace_all(r"\s+", " ").str.strip_chars()

        # 4. Validity masks -- fully vectorized boolean operations
        has_digit = s.str.contains(r"\d")
        is_empty = s.str.len_chars().eq(0)
        is_invalid = has_digit | is_empty

        return df.with_columns([
            s.alias("sentence"),
            pl.when(is_invalid).then(0).otherwise(pl.col("up_votes")).alias("up_votes"),
            pl.when(is_invalid).then(2).otherwise(pl.col("down_votes")).alias("down_votes"),
        ])

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
