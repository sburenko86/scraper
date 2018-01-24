import requests
from lxml import html
import sys
import os
import logging
import urlparse


logging.basicConfig(format='%(message)s', level=logging.INFO)
folder_name = 'downloaded/'


def create_base_folder(folder):
    logging.info('Create base folder for downloading')
    if not os.path.exists(folder):
        os.mkdir(folder)


def main():
    logging.info('Getting web site')
    response = requests.get(param_value,
                            headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) '
                                                   'Gecko/20100101 Firefox/57.0'})

    logging.info('Ensure that a program halts if a bad download occurs')
    response.raise_for_status()

    logging.info('Getting parsed body')
    parsed_body = html.fromstring(response.content)
    links = parsed_body.xpath('//*/@src | //link/@href')

    logging.info('Converting all relative references to absolute')
    links = [urlparse.urljoin(response.url, url) for url in links]

    create_base_folder(folder_name)
    for url in links:
        try:
            logging.info('Downloading file: %s' % url)
            with open(folder_name + url.split('/')[-1], 'wb') as f:
                f.write(requests.get(url).content)
        except Exception:
            logging.info('Have some exceptions during loading file')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        logging.info("Please, use next format: python file.py --site 'link_to_site'")
    else:
        param_name = sys.argv[1]
        protocol = 'https://'
        param_value = protocol + sys.argv[2] if param_name == '--site' else protocol + sys.argv[1]
        response = requests.head(param_value)
        if response.status_code == '504':
            protocol = 'http://'
        param_value = protocol + sys.argv[2] if param_name == '--site' else protocol + sys.argv[1]
        main()
