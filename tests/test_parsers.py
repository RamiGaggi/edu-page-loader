"""Test parsers."""

import argparse

from page_loader.parsers import create_arg_parser, parse_file_name


def test_parse_file_name():
    """Test parse file names."""
    url1 = 'https://ru.hexlet.io/courses'
    url2 = 'https://www.google.ru/Ch=Eck'
    url3 = 'https://test.ru/smth/file.js'
    assert parse_file_name(url1) == 'ru-hexlet-io-courses.html'
    assert parse_file_name(url2) == 'www-google-ru-ch-eck.html'
    assert parse_file_name(url3, files=True) == 'test-ru-smth-file.js'


def test_create_arg_parser():
    """Test creating arg parser."""
    arguments = argparse.Namespace(log='ERROR', output=None, url='http://google.ru')
    assert create_arg_parser(['http://google.ru']) == arguments
