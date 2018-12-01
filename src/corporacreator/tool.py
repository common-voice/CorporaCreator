import sys
import logging

from corporacreator import Corpora
from corporacreator import parse_args
from corporacreator import setup_logging


_logger = logging.getLogger(__name__)

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Creating corpora...")
    corpora = Corpora(args)
    corpora.create()
    _logger.info("Created corpora.")
    _logger.info("Saving corpora...")
    corpora.save()
    _logger.info("Saved corpora.")


def run():
    """Entry point for create-corpora
    """
    main(sys.argv[1:])
