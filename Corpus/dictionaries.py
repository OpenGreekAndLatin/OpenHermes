#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys

sys.path.append("../")

import os
from Tools.download import File
from Tools.download import Copyrighted


class Dictionary(object):
    def __init__(self):
        self.sourcelang = None
        self.targetlang = None
        self.url = None

        pass

    def install(self):
        raise NotImplementedError("Install is not installed")

    def convert(self):
        raise NotImplementedError("Install is not installed")

    def search(self):
        raise NotImplementedError("Install is not installed")

    def download(self):
        filename = os.path.basename(self.url)
        self.download = File(self.url, "Files", filename)
        return self.download.check(force=True)


class Gaffiot(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        #self.url = "http://outils.biblissima.fr/collatinus/ressources/Gaffiot_1934.djvu"
        self.url = "http://sourceforge.net/projects/digital-gaffiot/?source=navbar"
        self.sourcelang = "la"
        self.targetlang = "fr"

    def install(self):
        self.download()

    def download(self):
        FileInstance = Copyrighted("Files", "gaffiot.xml",
                                   origin="Dictionary/")
        FileInstance.check(force=True)


class LS(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        #Based on Biblissima
        self.url = "http://outils.biblissima.fr/collatinus/ressources/Lewis_and_Short_1879.xml"
        self.sourcelang = "la"
        self.targetlang = "en"

    def install(self):
        self.download()


class Georges(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        #Based on Biblissima
        self.url = "http://outils.biblissima.fr/collatinus/ressources/Georges_1913.xml"
        self.sourcelang = "de"
        self.targetlang = "fr"

    def install(self):
        self.download()


class Calonghi(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        #Based on Biblissima
        self.url = "http://outils.biblissima.fr/collatinus/ressources/Calonghi_1898.djvu"
        self.sourcelang = "de"
        self.targetlang = "it"


    def install(self):
        self.download()


class LSJ(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        #Based on Perseus Digital Library
        self.url = "https://github.com/PerseusDL/lexica/tree/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/*.xml"
        self.sourcelang = "gr"
        self.targetlang = "en"

    def install(self):
        self.download()

    def download(self):
        files = os.path.basename(self.url)
        self.download = File(self.url, "Files", files)
        return self.download.check(force=True)

    def convert(self):
        from bs4 import BeautifulSoup as b_soup
        #from glob import glob
        #from tkinter.filedialog import askdirectory
        from collections import defaultdict

        #since we have the url above, we may not need this stuff
        #I implemented it for local files
        #I guess it should be implemented in the download function
        #but I don't understand exactly what is happening there
        #orig = askdirectory(title='Where are your original XML lexicon files?')
        #files = glob('/'.join([orig, '*.xml']))

        tr_dict = defaultdict(list)
        for file in files:
            with open(file) as f:
                text = f.read()
            soup = b_soup(text)
            for word in soup.find_all('entryfree'):
                for s in word.find_all('sense'):
                    try:
                        tr_dict[word.orth.text].append(s.tr.text)
                    except:
                        continue