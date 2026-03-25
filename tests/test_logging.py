"""Tests for corporacreator.logging (unchanged from v1)."""

import logging

from corporacreator import setup_logging


class TestSetupLogging:
    def test_does_not_raise(self):
        """setup_logging should not raise for valid log levels."""
        setup_logging(logging.INFO)
        setup_logging(logging.DEBUG)

    def test_format_contains_cc_py_tag(self):
        """Log format should contain the CC-PY tag for bundler integration."""
        # Remove existing handlers so basicConfig can install a fresh one
        root = logging.getLogger()
        original_handlers = root.handlers[:]
        root.handlers.clear()
        try:
            setup_logging(logging.INFO)
            assert any(
                "CC-PY" in getattr(h, "formatter", None)._fmt
                for h in root.handlers
                if hasattr(getattr(h, "formatter", None), "_fmt")
            )
        finally:
            # Restore original handlers for pytest
            root.handlers = original_handlers
