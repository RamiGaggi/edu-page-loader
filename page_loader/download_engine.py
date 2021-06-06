"""Tools for page downloading."""

import os

import requests
from page_loader.parsers import parse_file_name


def download(url, output_path=None):
    """Download a web page.

    Args:
        url (str): Page url.
        output_path (str, optional): Defaults to None (current working dir).
    """
    req = requests.get(url)

    if not output_path:
        output_path = os.getcwd()

    file_name = parse_file_name(url)
    path = os.path.join(output_path, file_name)
    with open(path, 'w') as html:
        html.write(req.text)
