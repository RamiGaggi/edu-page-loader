"""Test page downloading."""

import os
import tempfile

import pytest
import requests
import requests_mock
from page_loader.download_engine import download

TEST_ADRESS = 'http://test1/test2/tes&t3/test4/tes%t5.com'


@pytest.fixture
def source_page():
    """Return source page in str format."""
    with open('tests/fixtures/source_page.html', 'r') as html:
        return html.read()


@pytest.fixture
def expected_page():
    """Return expeceted page in str format."""
    with open('tests/fixtures/expected_page.html', 'r') as html:
        return html.read()


def test_download_cwd(source_page, expected_page):
    """Success download of a web page in cwd."""
    cwd = os.getcwd()
    with requests_mock.Mocker() as mock:
        mock.get(TEST_ADRESS, text=source_page)
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            download(TEST_ADRESS)
            os.chdir(cwd)
            with open(tmp + '/test1-test2-tes-t3-test4-tes-t5-com.html') as res:
                assert res.read() == expected_page


def test_download_cwd2(source_page, expected_page):
    """Success download of a web page in choosen dir."""
    with requests_mock.Mocker() as mock:
        mock.get(TEST_ADRESS, text=source_page)
        with tempfile.TemporaryDirectory() as tmp:
            download(TEST_ADRESS, output_path=tmp)
            with open(tmp + '/test1-test2-tes-t3-test4-tes-t5-com.html') as res:
                assert res.read() == expected_page


def test_download_nonexistent_res():
    """Download of non-existent web page."""
    with pytest.raises(requests.exceptions.ConnectionError):
        download('http://test-none-xisten.com')
