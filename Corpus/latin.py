#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import sys for relative import
import sys
sys.path.append("../")

from Corpus.dictionaries import Dictionary
from Tools.download import Copyrighted

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
		FileInstance = Copyrighted("Files", "gaffiot.xml", origin = "Dictionary/")
		FileInstance.check(force = True)

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
