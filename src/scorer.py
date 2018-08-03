# TODO: better docstrings
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import requests
from bs4 import BeautifulSoup
import os
# noinspection PyUnresolvedReferences
from .store import Storage


class Scorer:
    def __init__(self, fp):
        self._store = Storage().load(fp) if os.path.isfile(fp) else Storage()
        self.fp = fp

        # TODO: make the score matrix part of the backing store, so we don't have to recompute on each initialization.
        if self.ls():
            self.score()
        else:
            self._score = np.array([], dtype=np.uint)

    def score(self):
        """
        Scores the current media list.

        Returns a similarity matrix. The mapping of indices to keys is the same as in the Store.
        """
        select = self._store.media_mapping

        row_keys = list(select.values())
        relevant_submatrix = pairwise_distances(self._store.matrix[row_keys], metric='cosine')
        self._score = relevant_submatrix

    def get(self, media):
        media_idx = self._store.media_mapping[media]

        row_keys = list(self._store.media_mapping.keys())
        media_row = self._score[media_idx]

        ret = {row_key: row for (row_key, row) in zip(row_keys, media_row)}
        del ret[media]
        return ret

    def top(self, media, n=5):
        """Returns the N most similar media."""
        media_scores = self.get(media)
        top_n_idxs = np.argsort(list(media_scores.values()))[:n]
        return {row_key: row for (row_key, row) in np.array(list(media_scores.items()))[top_n_idxs]}

    def has(self, media):
        """Checks if the given media is already in the Scorer."""
        return media in self._store.media_mapping.keys()

    def append(self, media):
        """Appends a media not already in the store to list."""
        if media in self._store.media_mapping.keys():
            raise ValueError(f"{media} is already included.")
        else:
            r = requests.get(media)
            r.raise_for_status()

            # TODO: blacklist or deselect certain uninformative links like "Main/Home" and friends.
            soup = BeautifulSoup(r.content, 'html.parser')
            links = soup.find_all("a", href=True)
            trope_links = [l['href'] for l in links if ('pmwiki/pmwiki.php/Main/' in l['href'])]
            # media_links = [l['href'] for l in links if
            #                ('pmwiki/pmwiki.php/' in l['href'] and '/Main/' not in l['href'])]

            self._store.add_media(media)
            self._store.update_media(media, trope_links)

    def ls(self):
        """Returns the list of medias contained in the Scorer."""
        return self._store.media_mapping.keys()

    def compare(self, a, b):
        """Returns the similarity score for two pieces of media."""
        include = self._store.media_mapping.keys()
        if a not in include:
            raise ValueError(f"{a} is not in the Scorer.")
        elif b not in include:
            raise ValueError(f"{b} is not in the Scorer.")

        a_idx, b_idx = self._store.media_mapping[a], self._store.media_mapping[b]
        return self._score[a_idx][b_idx]

    def commit(self):
        """Saves the current data to persistent memory."""
        self._store.store(self.fp)
