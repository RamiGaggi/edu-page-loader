"""Tools for page downloading."""

import logging
import os
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from page_loader.parsers import parse_file_name
from progress.bar import Bar


class KnownError(Exception):
    pass


def write_resource(path, res_content, content_type='bytes'):
    """Write content to file.

    Args:
        path (str): Path to file.
        res_content (bytes): Content of file.

    Raises:
        KnownError: Error.

    Returns:
        str: Path to resource.
    """
    try:
        logging.debug('Write_resource %s', path)
        if content_type == 'bytes':
            with open(path, 'wb') as resource:
                resource.write(res_content)
                return path
        else:
            with open(path, 'w+') as resource:
                resource.write(res_content)
                return path
    except OSError as err:
        logging.error(
            'The specified path does not exist: %s',
            os.path.dirname(path),
        )
        raise KnownError from err


def is_domain(domain_url=None):
    """Check url for domain.

    Args:
        domain_url (str): URL of domain resource.

    Returns:
        boolean: True if url in domain and exist, else False.
    """
    def inner(attr_url):  # noqa: WPS430
        attr = urlparse(attr_url)
        domain = urlparse(domain_url)
        return not attr.netloc or attr.netloc == domain.netloc
    return inner


def create_dir(path):
    """Create directory in specified path.

    Args:
        path (str): Path to directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def download(url, output_path=None, files=False):  # noqa: WPS210
    """Download resoursce.

    Args:
        url (str): Page URL.
        output_path (str, optional): Existing path. Defaults to None.
        files (bool, optional): True if downloading page resources.

    Raises:
        KnownError: Error.

    Returns:
        str: Path to page.
    """
    # Check for output path.
    if output_path is None:
        output_path = os.getcwd()

    # Parse paths, names, get content.
    file_name = parse_file_name(url, files=True) if files else parse_file_name(url)  # noqa: E501
    resource_path = os.path.join(output_path, file_name)
    path_to_file = (os.path.normpath(resource_path)).split(os.sep)
    rel_path_to_file = os.path.join(path_to_file[-2], path_to_file[-1])
    # Check for URL. Handling  resource existance.
    try:
        req = requests.get(url, stream=True)
    except Exception as err:
        logging.debug(err)

        if files:
            logging.error('Invalid URL page resource!')
            return 'Error occured'

        logging.error('Failed to establish a new connection, check URL!')
        raise KnownError from err

    res_content = req.content.strip()

    # Check connection and write. Handling errors [404, 500, ...].
    if req and not files:
        write_resource(resource_path, res_content)
    elif req and files:
        write_resource(resource_path, res_content)
        return rel_path_to_file
    else:
        logging.error(
            'Resource is unavailable: %s',
            url,
        )
        if not files:
            raise KnownError('Resource is unavailable!')
        return 'Error occured'

    # Creating dir for local resources.
    files_path = resource_path[:-5] + '_files'
    logging.debug('Files path: %s', files_path)
    create_dir(files_path)

    # Soap parse.
    soup_html = BeautifulSoup(res_content, features='html.parser')
    is_url_domain = is_domain(domain_url=url)
    images = soup_html('img', src=is_url_domain)  # noqa: E501, WPS221
    links = soup_html('link', href=is_url_domain)
    scripts = soup_html('script', src=is_url_domain)

    # Make local resources point to downloaded files.
    local_resources = (*images, *links, *scripts)
    result_bar = Bar('Loading page resource', max=len(local_resources))
    for tag in (*images, *links, *scripts):
        result_bar.next()  # noqa: B305
        if tag.name == 'link':
            full_tag_url = urljoin(url, tag['href'])
            tag['href'] = download(full_tag_url, files_path, files=True)
            logging.info('\n \u2713 %s', full_tag_url)
        else:
            full_tag_url = urljoin(url, tag['src'])
            tag['src'] = download(full_tag_url, files_path, files=True)
            logging.info('\n \u2713 %s', full_tag_url)

    result_bar.finish()
    logging.debug('Page path: %s', resource_path)
    return write_resource(resource_path, soup_html.prettify(formatter='html5'), content_type='soup')
