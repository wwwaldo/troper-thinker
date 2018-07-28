#!/usr/bin/python3
import sys
from scorer import Scorer
from tqdm import tqdm

media_list_fp = sys.argv[1]
data_store_fp = sys.argv[2]

with open(media_list_fp) as f:
    ls = [t for t in f.read().splitlines()]

sc = Scorer(data_store_fp)

ls = set(ls).difference(sc.ls())
for idx, media in enumerate(tqdm(ls)):
    sc.append(media)
    if idx % 10 == 0:
        sc.store()
sc.store()
