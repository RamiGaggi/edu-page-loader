"""Test page downloading."""

import os
import tempfile

import pytest
import requests_mock
from page_loader.download_engine import KnownError, download

TEST_ADRESS = 'http://mytest.com/caramba123'
TEST_CSS = 'http://mytest.com/caramba123/assets/application.css'
TEST_PNG = 'http://mytest.com/caramba123/assets/nodejs.png'
TEST_HTML = 'http://mytest.com/caramba123/assets/courses.html'


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


@pytest.fixture
def resource_page_css():
    """Return css in str format."""
    with open('tests/fixtures/assets/application.css', 'r') as css:
        return css.read()


@pytest.fixture
def resource_page_png():
    """Return png in str format."""
    with open('tests/fixtures/assets/nodejs.png', 'r', encoding='ISO-8859-1') as png:
        return png.read()


@pytest.fixture
def resource_page_html():
    """Return html in str format."""
    with open('tests/fixtures/assets/courses.html', 'r') as html:
        return html.read()


def test_download_in_cwd(
    source_page,
    expected_page,
    resource_page_png,
    resource_page_css,
    resource_page_html,
):
    """Success download of a web page in cwd."""
    cwd = os.getcwd()
    try:
        with requests_mock.Mocker() as mock:
            mock.get(TEST_ADRESS, text=source_page)
            mock.get(TEST_PNG, text=resource_page_png)
            mock.get(TEST_CSS, text=resource_page_css)
            mock.get(TEST_HTML, text=resource_page_html)

            with tempfile.TemporaryDirectory() as tmp:
                os.chdir(tmp)
                path = download(TEST_ADRESS)
                files_path = path[:-5] + '_files'
                with open(path) as res:
                    assert res.read() == expected_page
                with open(os.path.join(
                    files_path,
                    'mytest-com-caramba123-assets-application.css',
                )) as css:
                    assert css.read() == resource_page_css
                with open(os.path.join(
                    files_path,
                    'mytest-com-caramba123-assets-courses.html',
                )) as html:
                    assert html.read() == resource_page_html
                with open(os.path.join(
                    files_path,
                    'mytest-com-caramba123-assets-nodejs.png',
                )) as png:
                    assert png.read() == resource_page_png
    finally:
        os.chdir(cwd)


def test_download_in_dir(
    source_page,
    expected_page,
    resource_page_png,
    resource_page_css,
    resource_page_html,
):
    """Success download of a web page in choosen dir."""
    with requests_mock.Mocker() as mock:
        mock.get(TEST_ADRESS, text=source_page)
        mock.get(TEST_PNG, text=resource_page_png)
        mock.get(TEST_CSS, text=resource_page_css)
        mock.get(TEST_HTML, text=resource_page_html)

        with tempfile.TemporaryDirectory() as tmp:
            path = download(TEST_ADRESS, output_path=tmp)
            files_path = path[:-5] + '_files'
            with open(path) as res:
                assert res.read() == expected_page
            with open(os.path.join(
                files_path,
                'mytest-com-caramba123-assets-application.css',
            )) as css:
                assert css.read() == resource_page_css
            with open(os.path.join(
                files_path,
                'mytest-com-caramba123-assets-courses.html',
            )) as html:
                assert html.read() == resource_page_html
            with open(os.path.join(
                files_path,
                'mytest-com-caramba123-assets-nodejs.png',
            )) as png:
                assert png.read() == resource_page_png


def test_download_nonexistent_res():
    """Download of non-existent web page."""
    with pytest.raises(KnownError):
        download('http://test-none-xisten.com')


def test_download_error_dir(source_page):
    """Download of non-existent web page."""
    with pytest.raises(KnownError):
        with requests_mock.Mocker() as mock:
            mock.get(TEST_ADRESS, text=source_page)
            download(TEST_ADRESS, output_path='./test1/t!@#!@$123')


def test_download_res_not_found():
    """Download of non-existent resource."""
    with requests_mock.Mocker() as mock:
        mock.get(TEST_ADRESS, text='data', status_code=400)  # noqa:WPS432
        assert download(TEST_ADRESS) == 'ERROR'
