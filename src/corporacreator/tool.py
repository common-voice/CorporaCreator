import sys
import logging
import argparse

from corporacreator import Corpora
from corporacreator import __version__
from corporacreator import setup_logging

__license__ = "mpl"
__author__ = "kdavis-mozilla"
__copyright__ = "kdavis-mozilla"
_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Creates tsv files for Common Voice corpora")
    parser.add_argument(
        '--version',
        action='version',
        version='CorporaCreator {ver}'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        required=False,
        help="set loglevel to INFO",
        dest="loglevel",
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        action='store_const',
        required=False,
        help="set loglevel to DEBUG",
        dest="loglevel",
        const=logging.DEBUG)
    parser.add_argument(
        '-f',
        '--file',
        required=True,
        help="Path to the Common Voice tsv for all languages",
        dest="tsvfile")
    return parser.parse_args(args)


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
