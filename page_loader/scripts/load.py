#!/usr/bin/env python

"""Main script."""

from page_loader.download_engine import download
from page_loader.parsers import create_arg_parser


def main():
    """Run the programm."""
    args = create_arg_parser()
    url = args.url
    output_path = args.output
    download(url, output_path)


if __name__ == '__main__':
    main()
