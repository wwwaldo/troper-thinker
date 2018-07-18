import numpy as np
import pdb # the python debugger

initial_tropes_size = 26000 
# wc tropes.txt was 25855 last we checked
_debug = True

class Storage:
    """
    Store trope data.
    """

    @staticmethod
    def load(filename):
        """
        load from an existing pickle file. 
        """
        with open(filename, "rb") as file:
            return pickle.load(file)

    def store(self, filename):
        with open(filename, "wb") as file:
            # pickle throws an error if life is bad
            pickle.dump(self, file) 
        return

    def __init__(self):
        self.num_tropes = 0 
        self.num_media = 0
        self.trope_mapping = dict()
        self.media_mapping = dict()
        self.matrix = np.zeros((1,1), dtype=np.int8) # fill this in using populate.
        return

    def __str__(self):
        return f"(#Tropes {self.num_tropes} #Media {self.num_media}) \n {self.trope_mapping} \n {self.media_mapping} \n {self.matrix}"

    def populate_from_text(self, filename):
        # assumes: file contains only valid URLs and possibly newlines
        with open(filename, "r") as file: 
            urls = file.readlines()
            urls = (url.strip() for url in urls if url.strip()) # preprocessing

            tropes_added = 0 
            for url in urls:
                token = url.split('/')[-1] 
                tropes_added += self.add_trope(token)

            if _debug:
                print(f"Added {tropes_added} tropes") 
            return

    def expand(self, dimension):
        # dimension == "tropes" or "media"
        if dimension == "tropes":
            self.matrix = np.resize(self.matrix, (np.size(self.matrix, 0), 2 * np.size(self.matrix, 1)))
        elif dimension == "media":
            self.matrix = np.resize(self.matrix, (2 * np.size(self.matrix, 0), np.size(self.matrix, 1)))
        return

    def add_trope(self, trope):
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

            self.trope_mapping[trope] = self.num_tropes

            return 1

    def add_media(self, media):
        # add a media to self. 

        if media in self.media_mapping:
            return 0
        else:
            self.num_media += 1
            if self.num_media > np.size(self.matrix, 1):
                self.expand("media")

            self.media_mapping[media] = self.num_media

            return 1

    def update(self, trope, medialist):
        # input: dict of Media strings, with scores, and a trope name.
        # logs errors. permissively assumes media strings correspond to valid media names, which are unique identifiers. creates new entries in internal representation if media is not found.
        if trope in self.trope_mapping:
            trope_index = self.trope_mapping[trope]

            for media in medialist.keys():
                if not media in self.media_mapping:
                    self.add_media(media)

                media_index = self.media_mapping[media]
                recorded_score = medialist[media]
                self.matrix[media_index][trope_index] = recorded_score
        else:
            if _debug:
                print(f"{trope} not found")

        return

    def export(self, fname="trope-data.csv"): 
        # export self as csv
        raise Exception("Function not implemented")
        return

def query(self, trope):
    raise Exception("Function not implemented")
    return

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

    # try adding media.

    return

if __name__ == "__main__":
    print("Hello world")
    import doctest
    doctest.testmod() # run doctests.

    main()

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




