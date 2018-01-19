import requests
from lxml import html
import sys
import urlparse
import os

folder_name = 'downloaded/'


def create_base_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def main():
    response = requests.get(param_value,
                            headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) '
                                                   'Gecko/20100101 Firefox/57.0'})
    parsed_body = html.fromstring(response.content)
    links = parsed_body.xpath('//*/@src | //link/@href')
    create_base_folder(folder_name)
    for url in links:
        try:
            with open(folder_name + url.split('/')[-1], 'wb') as f:
                f.write(requests.get(url).content)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            pass


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Please, use next format: python file.py --site 'link_to_site'"
    else:
        param_name = sys.argv[1]
        param_value = sys.argv[2] if param_name == '--site' else sys.argv[1]
        main()
