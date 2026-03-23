import sys
import logging


def setup_logging(level):
    """Setup basic logging.

    When CC runs as a subprocess of the bundler, its stdout is captured and
    re-emitted by Node with the bundler's own timestamp and level prefix.
    The format here uses a short "CC-PY" tag so log lines are clearly
    distinguishable from Node-side "CC" log lines in the aggregated output.

    Standalone:  [2026-03-22 18:07:51] INFO CC-PY corpora: Parsing tsv file...
    Via bundler: [pod|ts] INFO [ps] CC [2026-03-22 18:07:51] INFO CC-PY corpora: Parsing tsv...

    Args:
      level (int): minimum log level for emitting messages
    """
    fmt = "[%(asctime)s] %(levelname)s CC-PY %(module)s: %(message)s"
    logging.basicConfig(
        level=level, stream=sys.stdout, format=fmt, datefmt="%Y-%m-%d %H:%M:%S"
    )
