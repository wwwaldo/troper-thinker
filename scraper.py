import urllib.request
from tropes import TropeDef
from bs4 import BeautifulSoup
import re
import pickle
import os.path

def scrape_types():
    raw_html = urllib.request.urlopen('http://tvtropes.org/pmwiki/browse.php')
    soup = BeautifulSoup(raw_html, 'html.parser')

    media_type_div = soup.find('div', id='media-namespaces')
    media_type_checkboxes = media_type_div.find_all('input')

    type_list = [media_type_box['value'] for media_type_box in media_type_checkboxes]
    return type_list

def scrape_tropedef(type_list, url):
    # Jumping The Shark defines its media examples in Folders. TODO we have not yet accounted
    # for trope pages whose examples are split into separate pages of the site, i.e. Tsundere
    raw_html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(raw_html, 'html.parser')

    trope_def = TropeDef(soup.title.string)

    all_links = soup.find_all('a', href=re.compile('^.*/(' + '|'.join(type_list) + ')/.*$'))
    print(type_list)
    print(all_links)

    print(trope_def)

if __name__ == "__main__":
    # Retrieve the full TVTropes Media Types list.
    type_list = []

    # If we don't have it yet, scrape it
    if not os.path.exists('.types.pickle'):
        type_list = scrape_types()
        with open('.types.pickle', 'wb') as f:
            pickle.dump(type_list, f)

    # Otherwise, it should be unpickled
    else:
        with open('.types.pickle', 'rb') as f:
            type_list = pickle.load(f)

    scrape_tropedef(type_list, 'http://tvtropes.org/pmwiki/pmwiki.php/Main/JumpingTheShark')
