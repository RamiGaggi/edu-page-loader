#!/usr/bin/env python

"""Main script."""

import logging

from page_loader.download_engine import download
from page_loader.parsers import create_arg_parser


def main():
    """Run the programm."""  # noqa: DAR401
    args = create_arg_parser()
    url = args.url
    output_path = args.output
    numeric_level_log = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level_log, int):
        raise ValueError('Invalid log level: %s' % numeric_level_log)

    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=numeric_level_log,
    )

    logging.info('Starting...')
    res_path = download(url, output_path)
    if res_path == 'ERROR':
        print("Page wasn't successfully downloaded")
    else:
        print("Page was successfully downloaded into '{0}'".format(res_path))
    logging.info('End')


if __name__ == '__main__':
    main()
