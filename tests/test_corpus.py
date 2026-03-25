"""Tests for corporacreator.corpus (v1.5 Polars rewrite)."""

import types

import polars as pl
import pytest

from corporacreator import Corpus


def _make_corpus(rows_data, locale="en", duplicate_sentence_count=1):
    """Helper: build a Corpus from a list of (client_id, sentence, up, down) tuples."""
    full_rows = []
    for i, (cid, sentence, up, down) in enumerate(rows_data):
        full_rows.append({
            "client_id": cid,
            "path": f"{cid}/audio_{i}.mp3",
            "sentence_id": f"s{i}",
            "sentence": sentence,
            "sentence_domain": "",
            "up_votes": up,
            "down_votes": down,
            "age": "",
            "gender": "",
            "accents": "",
            "variant": "",
            "locale": locale,
            "segment": "",
        })
    df = pl.DataFrame(full_rows, schema={
        "client_id": pl.String,
        "path": pl.String,
        "sentence_id": pl.String,
        "sentence": pl.String,
        "sentence_domain": pl.String,
        "up_votes": pl.Int32,
        "down_votes": pl.Int32,
        "age": pl.String,
        "gender": pl.String,
        "accents": pl.String,
        "variant": pl.String,
        "locale": pl.String,
        "segment": pl.String,
    })
    args = types.SimpleNamespace(
        duplicate_sentence_count=duplicate_sentence_count,
    )
    return Corpus(args, locale, df)


class TestPartition:
    """Tests for Corpus._partition."""

    def test_validated(self):
        corpus = _make_corpus([
            ("c1", "good", 3, 1),  # up > down, sum > 1 -> validated
        ])
        corpus._partition()
        assert len(corpus.validated) == 1
        assert len(corpus.other) == 0
        assert len(corpus.invalidated) == 0

    def test_invalidated(self):
        corpus = _make_corpus([
            ("c1", "bad", 1, 3),  # down > up, sum > 1 -> invalidated
        ])
        corpus._partition()
        assert len(corpus.invalidated) == 1
        assert len(corpus.validated) == 0

    def test_other_low_votes(self):
        corpus = _make_corpus([
            ("c1", "dunno", 1, 0),  # sum <= 1 -> other
        ])
        corpus._partition()
        assert len(corpus.other) == 1
        assert len(corpus.validated) == 0

    def test_other_tied_at_one(self):
        corpus = _make_corpus([
            ("c1", "tied", 1, 1),  # up==1, down==1 -> other
        ])
        corpus._partition()
        assert len(corpus.other) == 1
        assert len(corpus.validated) == 0
        assert len(corpus.invalidated) == 0

    def test_invalidated_tied_high(self):
        corpus = _make_corpus([
            ("c1", "tied high", 2, 2),  # up==down, sum > 2 -> invalidated
        ])
        corpus._partition()
        assert len(corpus.invalidated) == 1

    def test_mixed(self):
        corpus = _make_corpus([
            ("c1", "good", 3, 0),      # validated
            ("c2", "bad", 0, 3),        # invalidated
            ("c3", "unknown", 0, 0),    # other
            ("c4", "tied", 1, 1),       # other
            ("c5", "also bad", 2, 2),   # invalidated (tied, sum > 2)
        ])
        corpus._partition()
        assert len(corpus.validated) == 1
        assert len(corpus.invalidated) == 2
        assert len(corpus.other) == 2


class TestPreprocessLocale:
    """Tests for Corpus._preprocess_locale."""

    def test_no_preprocessor_skips(self):
        corpus = _make_corpus([
            ("c1", "sentence", 3, 0),
        ], locale="ps")
        original = corpus.corpus_data["sentence"][0]
        corpus._preprocess_locale()
        assert corpus.corpus_data["sentence"][0] == original

    def test_cy_preprocessor_applied(self):
        corpus = _make_corpus([
            ("c1", "mae'n siwr iawn", 3, 0),
        ], locale="cy")
        corpus._preprocess_locale()
        # cy preprocessor replaces ' with '
        assert "\u2019" not in corpus.corpus_data["sentence"][0]
        assert "'" in corpus.corpus_data["sentence"][0]

    def test_preprocessor_invalidates_empty(self):
        """If preprocessor returns empty string, votes should be invalidated."""
        corpus = _make_corpus([
            ("c1", "valid text", 3, 0),
        ], locale="ky")
        # ky removes bullet, so "•" alone becomes empty
        corpus.corpus_data = corpus.corpus_data.with_columns(
            pl.lit("\u2022").alias("sentence")  # bullet only
        )
        corpus._preprocess_locale()
        assert corpus.corpus_data["up_votes"][0] == 0
        assert corpus.corpus_data["down_votes"][0] == 2


class TestCalculateSplitSizes:
    """Tests for Corpus._calculate_split_sizes (binary search)."""

    def test_zero_total(self):
        corpus = _make_corpus([])
        assert corpus._calculate_split_sizes(0) == (0, 0, 0)

    def test_small_total(self):
        corpus = _make_corpus([])
        train, dev, test = corpus._calculate_split_sizes(100)
        assert train + dev + test <= 100
        assert dev == test  # both are sample_size(train)

    def test_large_total(self):
        corpus = _make_corpus([])
        train, dev, test = corpus._calculate_split_sizes(5_000_000)
        assert train + dev + test <= 5_000_000
        assert dev == test
        # For large N, sample_size converges to ~16641
        assert 16000 <= dev <= 17000

    def test_matches_v1_brute_force(self):
        """Binary search result should match v1's linear scan for known values."""
        from corporacreator import sample_size

        corpus = _make_corpus([])

        for total in [10, 100, 1000, 50000, 100000]:
            train_v2, dev_v2, test_v2 = corpus._calculate_split_sizes(total)

            # Replicate v1 linear scan
            train_v1 = total
            for t in range(total, 0, -1):
                if 2 * int(sample_size(t)) + t <= total:
                    train_v1 = t
                    break
            dev_v1 = int(sample_size(train_v1))

            assert train_v2 == train_v1, f"Mismatch at total={total}"
            assert dev_v2 == dev_v1, f"Mismatch at total={total}"


class TestPostProcessValidated:
    """Tests for dedup + speaker split logic."""

    def test_split_produces_three_sets(self):
        # 20 clips from 5 speakers, all validated
        rows = []
        for speaker_idx in range(5):
            for clip_idx in range(4):
                rows.append((
                    f"speaker_{speaker_idx}",
                    f"sentence {speaker_idx}_{clip_idx}",
                    3, 0,
                ))
        corpus = _make_corpus(rows, duplicate_sentence_count=5)
        corpus._partition()
        del corpus.corpus_data
        corpus._post_process_validated()
        total = len(corpus.train) + len(corpus.dev) + len(corpus.test)
        assert total <= len(corpus.validated)

    def test_dedup_limits_sentences(self):
        # Same sentence from 5 speakers, duplicate_sentence_count=2
        rows = [
            (f"speaker_{i}", "same sentence", 3, 0)
            for i in range(5)
        ]
        corpus = _make_corpus(rows, duplicate_sentence_count=2)
        corpus._partition()
        del corpus.corpus_data
        corpus._post_process_validated()
        # train+dev+test should have at most 2 rows (dedup limit)
        total = len(corpus.train) + len(corpus.dev) + len(corpus.test)
        assert total <= 2

    def test_empty_validated(self):
        rows = [("c1", "bad", 0, 3)]  # invalidated, not validated
        corpus = _make_corpus(rows)
        corpus._partition()
        del corpus.corpus_data
        corpus._post_process_validated()
        assert len(corpus.train) == 0
        assert len(corpus.dev) == 0
        assert len(corpus.test) == 0


class TestSave:
    """Tests for Corpus.save output format."""

    def test_tsv_output_format(self, tmp_path):
        rows = [
            ("c1", "hello", 3, 0),
            ("c2", "world", 3, 0),
        ]
        corpus = _make_corpus(rows)
        corpus.create()
        corpus.save(str(tmp_path))

        out_dir = tmp_path / "en"
        assert out_dir.exists()

        # Check validated.tsv exists and is tab-separated
        validated_path = out_dir / "validated.tsv"
        assert validated_path.exists()
        content = validated_path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) >= 1  # at least header
        # Header should be tab-separated column names
        header_cols = lines[0].split("\t")
        assert "client_id" in header_cols
        assert "sentence" in header_cols

    def test_all_six_files_created(self, tmp_path):
        rows = [("c1", "hello", 3, 0)]
        corpus = _make_corpus(rows)
        corpus.create()
        corpus.save(str(tmp_path))
        out_dir = tmp_path / "en"
        for name in ["other", "invalidated", "validated", "train", "dev", "test"]:
            assert (out_dir / f"{name}.tsv").exists()
