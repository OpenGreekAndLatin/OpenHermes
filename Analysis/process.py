#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import pickle

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from Corpus.dictionaries import Shelf
from Analysis.computation import Computation


class OpenSynonyms(object):
    def __init__(self, corpus, algorythm):
        if not issubclass(corpus, (Shelf)):
            raise TypeError("Corpus is not a subclass of Corpus.dictionaries.Shelf")

        if not issubclass(algorythm, (Computation)):
            raise TypeError("algorythm is not a subclass of Analysis.computation.Computation")

        self.shelf = corpus
        self.corpus = self.shelf()
        self.corpus.check(force=True)
        self.algorythm = algorythm

        self.path = os.path.dirname(os.path.abspath(__file__))

    def search(self, POS, lemma):

        if not isinstance(POS, str):
            raise TypeError("POS should be a string, {0} given".format(type(POS)))

        if not isinstance(lemma, str):
            raise TypeError("lemma should be a string, {0} given".format(type(lemma)))

        if not self.results:
            self.analyse()
        if POS not in self.results:
            raise ValueError("This PartOfSpeach is not available in this Corpus")

        if lemma not in self.results[POS].index.values:
            raise ValueError("{0} is not in the values of {1}".format(lemma, POS))

        found = self.results[POS]
        found = found.sort(lemma, ascending=True)
        found = found[lemma]
        found = found[found > 0.0]
        found_subset = found[1:10]
        heads = found_subset.keys().tolist()
        found_subset = found_subset.tolist()

        return list(zip(heads, found_subset))

    def checkCacheAnalyse(self):
        return False

    def generate(self, force=False):
        """ Read and Generate the dictionaries """
        data = {}
        for lang in self.corpus.data:
            data[lang] = self.corpus.data[lang].convert(force=force)
        self.data = data
        return data

    def analyse(self, force=False, debug=False, path=None):
        if self.from_pickle(path):
            return self.results

        """ Run the algorythm on the corpus """
        self.instance = self.algorythm(self.data)
        self.instance.dictConvert()
        self.instance.similarity()

        self.results = self.instance.average

        self.to_pickle(debug=debug, path=path)
        return self.results

    def from_pickle(self, path=None, debug=False):
        if not path:
            path = self.path + "/../Cache/"
        path = "{0}OGL_{1}_{2}_average.pickle".format(path, self.algorythm.__name__, self.shelf.__name__)

        if not os.path.isfile(path):
            return False

        with open(path, "rb") as f:
            self.results = pickle.load(f)
            return self.results
        return False

    def to_pickle(self, path=None, debug=False):
        if not path:
            path = self.path + "/../Cache/"
        path = "{0}OGL_{1}_{2}_average.pickle".format(path, self.algorythm.__name__, self.shelf.__name__)

        with open(path, "wb") as f:
            pickle.dump(self.results, f)

        if debug is True:
            print ("Results saved to {0}".format(path))

    def to_csv(self, path=None, debug=False):
        for POS in self.results:
            if not path:
                path = self.path + "/Results/"

            path = "{0}OGL_{1}_{2}_{3}_average.csv".format(path, POS, self.algorythm.__name__, self.shelf.__name__)

            self.results[POS].to_csv(path)
            if debug is True:
                print ("Results saved to {0}".format(path))
