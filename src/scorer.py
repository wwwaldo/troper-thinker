import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import requests
from bs4 import BeautifulSoup


class Scorer:
    def __init__(self, store):
        # TODO: refactor to hide the store. Ask for a file pointer instead.
        self._store = store

        # TODO: make the score matrix part of the backing store, so we don't have to recompute on each initialization.
        self._score = self.score()

    def _get_store(self, media):
        """Returns a row of trope scores for a given media."""
        return self._store.matrix[self._store.media_mapping[media]]

    def score(self, medias=None):
        """
        Scores the given medias.

        Accepts a list of medias to enumerate over. By default, all medias included in the backing store will be
        used. However, you can choose to pass a shortlist via the `medias` parameter.

        Returns a similarity matrix. The mapping of indices to keys is the same as in the Store.
        """
        if medias:
            select = {name: self._get_store(name) for name in medias}
        else:
            select = self._store.media_mapping

        row_keys = list(select.values())
        relevant_submatrix = pairwise_distances(self._store.matrix[row_keys], metric='cosine')
        return relevant_submatrix

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
        top_n_idxs = np.argsort(list(media_scores.values()))[::-n]
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

            soup = BeautifulSoup(r.content, 'html.parser')
            links = soup.find_all("a", href=True)
            trope_links = [l['href'] for l in links if ('pmwiki/pmwiki.php/Main/' in l['href'])]
            # media_links = [l['href'] for l in links if
            #                ('pmwiki/pmwiki.php/' in l['href'] and '/Main/' not in l['href'])]

            self._store.add_media(media)
            self._store.update_media(media, trope_links)
