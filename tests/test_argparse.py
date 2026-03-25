"""Tests for corporacreator.argparse (unchanged from v1)."""

import pytest
from corporacreator import parse_args


class TestParseArgs:
    def test_required_args(self):
        args = parse_args(["-f", "input.tsv", "-d", "output/"])
        assert args.tsv_filename == "input.tsv"
        assert args.directory == "output/"

    def test_default_duplicate_count(self):
        args = parse_args(["-f", "input.tsv", "-d", "output/"])
        assert args.duplicate_sentence_count == 1

    def test_custom_duplicate_count(self):
        args = parse_args(["-f", "input.tsv", "-d", "output/", "-s", "3"])
        assert args.duplicate_sentence_count == 3

    def test_langs_option(self):
        args = parse_args(["-f", "input.tsv", "-d", "output/", "-l", "en", "de"])
        assert args.langs == ["en", "de"]

    def test_no_langs_default(self):
        args = parse_args(["-f", "input.tsv", "-d", "output/"])
        assert args.langs is None
