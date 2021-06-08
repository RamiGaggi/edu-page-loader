"""Tools for page downloading."""

import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from page_loader.parsers import parse_file_name


def write_resource(path, res_content):
    """Write content to file.

    Args:
        path (str): Path to file.
        res_content (bytes): Content of file.

    Returns:
        str: Path to resource.
    """
    with open(path, 'wb+') as resource:
        resource.write(res_content)
    return path


def is_domain(attr_url):
    """Check url for domain.

    Args:
        attr_url (str): URL of resource.

    Returns:
        boolean: True if url in domain and exist, else False.
    """
    url_parser = urlparse(attr_url)
    return not url_parser.netloc and attr_url is not None


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
        url ([type]): [description]
        output_path ([type], optional): [description]. Defaults to None.
        files (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    # Check for output path.
    if output_path is None:
        output_path = os.getcwd()

    # Parse paths, names, get content.
    file_name = parse_file_name(url, files=True) if files else parse_file_name(url)  # noqa: E501
    resource_path = os.path.join(output_path, file_name)
    req = requests.get(url, stream=True)
    res_content = req.content.strip()

    # Check connection and write.
    if req and not files:
        write_resource(resource_path, res_content)
    elif req and files:
        write_resource(resource_path, res_content)
        path = (os.path.normpath(resource_path)).split(os.sep)
        return os.path.join(path[-2], path[-1])
    else:
        return 'ERROR'

    # Creating dir for local resources.
    files_path = resource_path[:-5] + '_files'
    create_dir(files_path)

    # Soap parse.
    soup_html = BeautifulSoup(res_content, features='html5lib')
    images = soup_html('img', src=is_domain)  # noqa: E501, WPS221
    links = soup_html('link', href=is_domain)
    scripts = soup_html('script', src=is_domain)

    # Make local resources point to downloaded files.
    for tag in (*images, *links, *scripts):
        if tag.name == 'link':
            full_tag_url = url + tag['href']
            tag['href'] = download(full_tag_url, files_path, files=True)
        else:
            full_tag_url = url + tag['src']
            tag['src'] = download(full_tag_url, files_path, files=True)

    return write_resource(resource_path, soup_html.encode(formatter='html5'))
