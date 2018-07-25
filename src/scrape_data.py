#!/usr/bin/python3
import sys
import os
from store import Storage
import requests
from bs4 import BeautifulSoup


tropes_list_fp = sys.argv[1]
data_store_fp = sys.argv[2]

with open(tropes_list_fp) as f:
    ls = [t for t in f.read().splitlines()]


if os.path.isfile(data_store_fp):
    store = Storage().load(data_store_fp)
    priors = store.tropes
    ls = set(ls).difference(priors)
else:
    store = Storage()


for trope in ls:
    import pdb; pdb.set_trace()
    r = requests.get(trope)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all("a", href=True)
    trope_links = [l for l in links if ('https://tvtropes.org/pmwiki/pmwiki.php/Main/' in l['href'])]
    media_links = [l for l in links if ('https://tvtropes.org/pmwiki/pmwiki.php/' in l['href']
                                        and '/Main/' not in l['href'])]
    for idx, trope_link in enumerate(trope_links):
        trope = trope_link['href']
        store.add_trope(trope)

        if idx % 2 == 0:
            store.store(data_store_fp)