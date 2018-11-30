import sys
import logging

from corporacreator import Corpora
from corporacreator import parse_args
from corporacreator import setup_logging

__license__ = "mpl"
__author__ = "kdavis-mozilla"
__copyright__ = "kdavis-mozilla"
_logger = logging.getLogger(__name__)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting creation of corpora...")
    corpora = Corpora(args)
    corpora.create()
    corpora.save()
    _logger.info("Finished creation of corpora.")


def run():
    """Entry point for create-corpora
    """
    main(sys.argv[1:])
