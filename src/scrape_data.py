#!/usr/bin/python3
import sys
import os
from store import Storage
import requests
from bs4 import BeautifulSoup


media_list_fp = sys.argv[1]
data_store_fp = sys.argv[2]

with open(media_list_fp) as f:
    ls = [t for t in f.read().splitlines()]


if os.path.isfile(data_store_fp):
    store = Storage().load(data_store_fp)
    priors = store.tropes
    ls = set(ls).difference(priors)
else:
    store = Storage()


for media in ls:
    r = requests.get(media)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all("a", href=True)
    trope_links = [l['href'] for l in links if ('pmwiki/pmwiki.php/Main/' in l['href'])]
    media_links = [l['href'] for l in links if ('pmwiki/pmwiki.php/' in l['href'] and '/Main/' not in l['href'])]

    store.add_media(media)
    store.update_media(media, trope_links)

from scorer import Scorer
sc = Scorer(store)
import pdb; pdb.set_trace()
sc.top('https://tvtropes.org/pmwiki/pmwiki.php/Film/CitizenKane')