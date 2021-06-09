"""Parsers."""

import argparse
import re
from urllib.parse import urlparse


def parse_file_name(url, files=False):
    """Return file name in the specified format.

    Args:
        url (str): Page url.
        files (boolean): True for downloading local page resources.

    Returns:
        str: https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html
    """
    without_scheme = ''.join(urlparse(url)[1:])

    if re.search(r'\.[a-zA-Z]*$', without_scheme) and files:
        dot_split = without_scheme.split('.')
        dot_to_hyphen = '-'.join(dot_split[:-1])
        without_ext = re.sub('[^a-zA-Z0-9]', '-', dot_to_hyphen)
        file_name = without_ext + '.' + dot_split[-1]  # noqa:E501
    else:
        file_name = re.sub('[^a-zA-Z0-9]', '-', without_scheme) + '.html'
    return file_name.lower()


def create_arg_parser(args=None):
    """Parse arguments from CLI.

    Args:
        args: CLI args form input.

    Returns:
        Namespace object with arguments.
    """
    parser = argparse.ArgumentParser(description="""Downloads a page from the
                                     network and puts it in the specified
                                     existing directory""")
    parser.add_argument(
        '--log',
        metavar='\b',
        type=str,
        help='specify log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)',
        default='ERROR',
    )

    parser.add_argument(
        '-o',
        '--output',
        metavar='\b',
        type=str,
        help='output dir (default: current working directory)',
        default=None,
    )

    parser.add_argument('url', type=str)

    return parser.parse_args(args)
