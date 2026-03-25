"""Tests for corporacreator.tool (end-to-end integration)."""

import os

from conftest import make_row


class TestEndToEnd:
    """End-to-end test via tool.main."""

    def test_full_pipeline(self, tmp_tsv, tmp_path):
        from corporacreator.tool import main

        rows = [
            make_row(client_id="c1", sentence="hello world", up_votes=3, down_votes=0, locale="en"),
            make_row(client_id="c2", sentence="goodbye world", up_votes=3, down_votes=0, locale="en"),
            make_row(client_id="c3", sentence="bad clip", up_votes=0, down_votes=3, locale="en"),
            make_row(client_id="c4", sentence="unknown", up_votes=0, down_votes=0, locale="en"),
        ]
        tsv_path = tmp_tsv(rows)
        out_dir = str(tmp_path / "e2e_output")

        main(["-f", tsv_path, "-d", out_dir, "-l", "en", "-v"])

        en_dir = os.path.join(out_dir, "en")
        assert os.path.exists(en_dir)
        for name in ["other", "invalidated", "validated", "train", "dev", "test"]:
            fpath = os.path.join(en_dir, name + ".tsv")
            assert os.path.exists(fpath), f"Missing {name}.tsv"
