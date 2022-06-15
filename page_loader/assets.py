"""Collecting a list of resources with content for download"""

import os

from page_loader.logging_settings import log_error
from urllib.parse import urljoin, urlparse
from page_loader import url


def get_resources(data, link, dir):
    """Takes three arguments:
    'data' is html page data,
    'link' is link to download page,
    'dir' is path to the directory to save a content.
    Returns a list of resources to download.
    """

    TAGS_AND_ATTRIBUTES = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }
    resources = []

    for teg in data.find_all(TAGS_AND_ATTRIBUTES.keys()):

        attribute = TAGS_AND_ATTRIBUTES.get(teg.name)
        content = teg.get(attribute)
        if content is None:
            log_error.error(f"Attributes src weren't found in {teg}\n")
            continue
        if content.startswith('http'):
            if not urlparse(link).netloc == urlparse(content).netloc:
                log_error.error(f"Content was not downloaded because it's"
                                f' on a different host: {content}')
                continue
            content_link = content
        else:
            if not content.startswith('/'):
                content = '/' + content
            content_link = urljoin(link, content)
        resources.append(content_link)

        teg[attribute] = os.path.join(dir, url.to_filename(content_link))
    return resources