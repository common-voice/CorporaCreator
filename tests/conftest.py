"""Shared fixtures for CorporaCreator v1.5 tests."""

import os
import types

import pytest
import polars as pl


@pytest.fixture
def tmp_tsv(tmp_path):
    """Create a minimal clips.tsv file and return its path."""

    def _make(rows, filename="clips.tsv"):
        header = (
            "client_id\tpath\tsentence_id\tsentence\tsentence_domain\t"
            "up_votes\tdown_votes\tage\tgender\taccents\tvariant\tlocale\tsegment"
        )
        lines = [header] + ["\t".join(str(c) for c in row) for row in rows]
        path = tmp_path / filename
        path.write_text("\n".join(lines), encoding="utf-8")
        return str(path)

    return _make


@pytest.fixture
def make_args(tmp_path):
    """Create a mock args namespace matching corporacreator.parse_args output."""

    def _make(tsv_path, langs=None, duplicate_sentence_count=1):
        return types.SimpleNamespace(
            tsv_filename=tsv_path,
            directory=str(tmp_path / "output"),
            langs=langs,
            duplicate_sentence_count=duplicate_sentence_count,
            loglevel=None,
        )

    return _make


# -- Reusable row data --

def make_row(
    client_id="c1",
    path="c1/audio.mp3",
    sentence_id="s1",
    sentence="hello world",
    sentence_domain="",
    up_votes=2,
    down_votes=0,
    age="",
    gender="",
    accents="",
    variant="",
    locale="en",
    segment="",
):
    return (
        client_id, path, sentence_id, sentence, sentence_domain,
        up_votes, down_votes, age, gender, accents, variant, locale, segment,
    )
