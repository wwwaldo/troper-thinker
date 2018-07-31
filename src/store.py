import numpy as np
import pickle


initial_tropes_size = 26000 
# wc tropes.txt was 25855 last we checked
_debug = True


class Storage:
    """
    Store trope data.

    Attributes:
        num_tropes, num_media (int) -- number of tropes, media currently in this store (excluding aliases)
        trope, media (dict[string] : string) -- dict of tropes, media with corresponding unique name identifiers

        _trope_mapping, _media_mapping : internal representation of trope : matrix index mapping
        matrix : internal representation of tropes and media
    
    Methods:
        TODO -- document methods.

    """

    @staticmethod
    def load(filename):
        """
        Load from an existing pickle file.
        """
        with open(filename, "rb") as file:
            return pickle.load(file)

    def store(self, filename):
        with open(filename, "wb") as file:
            # pickle throws an error if life is bad
            pickle.dump(self, file) 

    def __init__(self):
        """
        Initialize an empty store.
        """
        self.num_tropes = 0 
        self.num_media = 0
        self.tropes = dict()
        self.media = dict()
        self.trope_mapping = dict()
        self.media_mapping = dict()
        self.matrix = np.zeros((1,1), dtype=np.int8)  # fill this in using populate.

    def __str__(self):
        return f"(#Tropes {self.num_tropes} #Media {self.num_media}) \n {self.trope_mapping} \n {self.media_mapping} " \
               f"\n {self.matrix}"
    
    # might 'deprecate' this later
    def populate_from_text(self, filename):
        # assumes: file contains only valid URLs and possibly newlines
        with open(filename, "r") as file: 
            urls = file.readlines()
            urls = (url.strip() for url in urls if url.strip())  # preprocessing

            tropes_added = 0 
            for url in urls:
                token = url.split('/')[-1] 
                tropes_added += self.add_trope(token)

            if _debug:
                print(f"Added {tropes_added} tropes") 

    def expand(self, dimension):
        """
        Method for dynamically resizing self.matrix. Internal use only. 
        """
        # dimension == "tropes" or "media"
        if dimension == "tropes":
            self.matrix = np.hstack([self.matrix, np.zeros(self.matrix.shape[0])[np.newaxis].T])
        elif dimension == "media":
            import pdb; pdb.set_trace()
            self.matrix = np.resize(self.matrix, (2 * np.size(self.matrix, 0), np.size(self.matrix, 1)))
            self.matrix[self.matrix.shape[0] // 2:] = 0

    def add_trope(self, trope):
        """
        Add a new trope to the store.

        TODO -- handle trope aliasing.
        """

        # add a trope to self. trope is a string.
        # returns: ntropes added to self.

        if trope in self.trope_mapping:
            if _debug:
                print(f"{trope} already in store")
            return 0
        else:
            self.num_tropes += 1
            if self.num_tropes > np.size(self.matrix, 1):
                self.expand("tropes")

            self.trope_mapping[trope] = self.num_tropes - 1

            return 1

    def add_media(self, media):
        """
        Add a new media to the store. 

        TODO -- refactor this function to account for media aliases.
        """
        # add a media to self. 

        if media in self.media_mapping:
            return 0
        else:
            self.num_media += 1
            if self.num_media > self.matrix.shape[0]:
                self.expand("media")

            self.media_mapping[media] = self.num_media - 1

            return 1
    
    def get_score(self, trope, media):
        """
        Get trope score for this trope-media pair.
        
        Return: score as np.int8 if both trope and media exist in store, otherwise None.
        """
        score = None
        # if trope in self.tropes and media in self.media:
        if trope in self.trope_mapping and media in self.media_mapping:
            trope_idx = self.trope_mapping[trope] # TODO -- refactor for aliasing
            media_idx = self.media_mapping[media]

            score = self.matrix[trope_idx][media_idx]
        return score

    def update_media(self, media, tropes):
        media_index = self.media_mapping[media]

        for trope in tropes:
            # TODO: maintain a blacklist?
            if trope not in self.trope_mapping:
                self.add_trope(trope)

            trope_index = self.trope_mapping[trope]
            self.matrix[media_index][trope_index] = 1

    def update(self, trope, media_scores):
        """
        Update a trope with media scores.

        Params:
        trope (string) -- Unique name identifier of this trope.
        media_scores dict[string] -- dictionary of media names : trope-media scores.
            a trope-media score is positive if trope is played straight in media
            and zero if trope is not invoked in media.
        
        Example:

        >>> store = Storage()
        >>> trope = "JumpingTheShark"
        >>> store.add_trope(trope)
        1
        >>> show = "TheSimpsons"
        >>> store.add_media(show)
        1
        >>> media_scores = {show : 1}
        >>> store.update(trope, media_scores)
        >>> print(store.get_score(trope, show))
        1
        
        Notes: Permissively assumes media strings correspond to valid media names, which are unique identifiers. 
        Creates new entries in internal representation if media is not found.
        """
        if trope in self.trope_mapping:
            trope_index = self.trope_mapping[trope]

            for media in media_scores.keys():
                if not media in self.media_mapping:
                    self.add_media(media)
                media_index = self.media_mapping[media]
                recorded_score = media_scores[media]
                self.matrix[media_index][trope_index] = recorded_score
        else:
            if _debug:
                print(f"{trope} not found")

    def export(self, fname="trope-data.csv"): 
        # export self as csv
        raise NotImplementedError

    def query(self, trope):
        raise NotImplementedError


def main():
    # create a new storage node.
    store = Storage()
    print(f"{store}")

    # add a single trope to the store.
    store.add_trope("Hello world")
    # add a single trope to the store.
    store.add_trope("Foo Bar Baz")
    print(f"{store}")
    ## bug --- Baz doesn't increase the column length. What?
    ## fixed --- np.resize(matrix, (dim, dim)) doesn't mutate matrix, returns newmatrix.

    # add a duplicate trope.
    store.add_trope("Hello world")
    print(f"{store}")

    # add a real file of tropes.
    store = Storage() #
    store.populate_from_text("tropes.txt")
    # print(f"{store}")
    # looks good!


if __name__ == "__main__":
    import doctest
    doctest.testmod() # run doctests.

    main()

    store = Storage()
    trope = "JumpingTheShark"
    store.add_trope(trope)
    show = "TheSimpsons"
    store.add_media(show)
    media_scores = {show : 1}
    store.update(trope, media_scores)
    print(store.get_score(trope, show))

"""
footnote

import store
import pdb
import importlib as imp

# in a loop
pdb.run(store.main())

# on change to main:
imp.reload(store)

footnote(2):
tried using ipdb by pip3 and ubuntu pkg install
pip3 fails installation (no sudo)
ubuntu pkg install works but is broken.
    cannot run ipdb.set_trace
    cannot run store.main() without importing store 
    in ipdb code snippet
    so ipdb does not inherit the interpreter context

footnote(3):
use :choose-tree to switch between panes and sessions in tmux.

"""
