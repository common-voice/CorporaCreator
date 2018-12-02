import logging
import argparse

from pkg_resources import get_distribution, DistributionNotFound


try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "CorporaCreator"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Creates tsv files for Common Voice corpora"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="CorporaCreator {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        required=False,
        help="set loglevel to INFO",
        dest="loglevel",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        action="store_const",
        required=False,
        help="set loglevel to DEBUG",
        dest="loglevel",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the Common Voice tsv for all languages",
        dest="tsv_filename",
    )
    parser.add_argument(
        "-d",
        "--directory",
        required=True,
        help="Directory in which to save the Common Voice corpora",
        dest="directory",
    )
    return parser.parse_args(args)
