"""Parsers."""

import argparse
import re


def parse_file_name(url):
    """Return file name in the specified format.

    Args:
        url (str): Page url.

    Returns:
        str: https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html
    """
    without_scheme = url.split('//')[1]
    file_name = (re.sub('[^a-zA-Z0-9]', '-', without_scheme) + '.html').lower()
    if file_name.startswith('www-'):
        return file_name[4:]
    return file_name


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
        '-o',
        '--output',
        metavar='\b',
        type=str,
        help='output dir (default: current working directory)',
        default=None,
    )
    parser.add_argument('url', type=str)
    return parser.parse_args(args)
