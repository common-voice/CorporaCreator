"""Tests for corporacreator.corpora (v1.5 Polars rewrite)."""

import polars as pl
import pytest

from corporacreator import Corpora
from corporacreator.corpora import _clean_sentence
from conftest import make_row


class TestCleanSentence:
    """Unit tests for _clean_sentence helper."""

    def test_plain_text_unchanged(self):
        assert _clean_sentence("hello world") == "hello world"

    def test_url_decode(self):
        assert _clean_sentence("caf%C3%A9") == "caf\u00e9"

    def test_html_tags_stripped(self):
        assert _clean_sentence("<b>bold</b> text") == "bold text"

    def test_html_entities_converted(self):
        assert _clean_sentence("a &amp; b") == "a & b"

    def test_no_percent_skips_unquote(self):
        # Sentences without % should pass through unquote unchanged
        assert _clean_sentence("normal sentence") == "normal sentence"

    def test_no_ampersand_skips_unescape(self):
        assert _clean_sentence("no entities here") == "no entities here"


class TestParseTsv:
    """Tests for Corpora._parse_tsv."""

    def test_parse_basic(self, tmp_tsv, make_args):
        rows = [
            make_row(sentence="hello world", up_votes=2, down_votes=0),
            make_row(client_id="c2", sentence="goodbye", up_votes=1, down_votes=1),
        ]
        path = tmp_tsv(rows)
        args = make_args(path)
        corpora = Corpora(args)
        df = corpora._parse_tsv()
        assert len(df) == 2
        assert df.schema["up_votes"] == pl.Int32
        assert df.schema["down_votes"] == pl.Int32

    def test_parse_columns(self, tmp_tsv, make_args):
        rows = [make_row()]
        path = tmp_tsv(rows)
        args = make_args(path)
        corpora = Corpora(args)
        df = corpora._parse_tsv()
        expected_cols = {
            "client_id", "path", "sentence_id", "sentence", "sentence_domain",
            "up_votes", "down_votes", "age", "gender", "accents", "variant",
            "locale", "segment",
        }
        assert set(df.columns) == expected_cols


class TestPreprocessCommon:
    """Tests for Corpora._preprocess_common."""

    def _preprocess(self, tmp_tsv, make_args, rows):
        path = tmp_tsv(rows)
        args = make_args(path)
        corpora = Corpora(args)
        df = corpora._parse_tsv()
        return corpora._preprocess_common(df)

    def test_digit_sentence_invalidated(self, tmp_tsv, make_args):
        rows = [make_row(sentence="has 123 digits", up_votes=5, down_votes=0)]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["up_votes"][0] == 0
        assert df["down_votes"][0] == 2

    def test_empty_sentence_invalidated(self, tmp_tsv, make_args):
        rows = [make_row(sentence="   ", up_votes=5, down_votes=0)]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["up_votes"][0] == 0
        assert df["down_votes"][0] == 2

    def test_valid_sentence_unchanged(self, tmp_tsv, make_args):
        rows = [make_row(sentence="good sentence", up_votes=3, down_votes=1)]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["sentence"][0] == "good sentence"
        assert df["up_votes"][0] == 3
        assert df["down_votes"][0] == 1

    def test_whitespace_normalized(self, tmp_tsv, make_args):
        rows = [make_row(sentence="  lots   of   space  ")]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["sentence"][0] == "lots of space"

    def test_html_stripped(self, tmp_tsv, make_args):
        rows = [make_row(sentence="<p>paragraph</p>")]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["sentence"][0] == "paragraph"

    def test_control_chars_stripped(self, tmp_tsv, make_args):
        rows = [make_row(sentence="hello\x00world")]
        df = self._preprocess(tmp_tsv, make_args, rows)
        assert df["sentence"][0] == "helloworld"


class TestCorporaCreateAndSave:
    """Integration tests for Corpora.create + save."""

    def test_single_locale_end_to_end(self, tmp_tsv, make_args, tmp_path):
        rows = [
            make_row(client_id="c1", sentence="first sentence", up_votes=3, down_votes=0, locale="en"),
            make_row(client_id="c2", sentence="second sentence", up_votes=3, down_votes=0, locale="en"),
            make_row(client_id="c3", sentence="third sentence", up_votes=0, down_votes=3, locale="en"),
        ]
        path = tmp_tsv(rows)
        args = make_args(path, langs=["en"])
        corpora = Corpora(args)
        corpora.create()
        corpora.save(args.directory)

        out_dir = tmp_path / "output" / "en"
        assert out_dir.exists()
        for name in ["other", "invalidated", "validated", "train", "dev", "test"]:
            assert (out_dir / f"{name}.tsv").exists()

    def test_invalid_locale_raises(self, tmp_tsv, make_args):
        rows = [make_row(locale="en")]
        path = tmp_tsv(rows)
        args = make_args(path, langs=["xx"])
        corpora = Corpora(args)
        with pytest.raises(Exception, match="do not exist"):
            corpora.create()
