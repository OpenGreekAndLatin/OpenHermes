#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import sys for relative import
import sys
sys.path.append("../")

from Tools.download import File

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

class Gaffiot(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		self.url = "http://outils.biblissima.fr/collatinus/ressources/Gaffiot_1934.djvu"
		self.sourcelang = "la"
		self.targetlang = "fr"

class LS(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		#Based on Biblissima
		self.url = "http://outils.biblissima.fr/collatinus/ressources/Lewis_and_Short_1879.xml"
		self.sourcelang = "la"
		self.targetlang = "en"

class Georges(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		#Based on Biblissima
		self.url = "http://outils.biblissima.fr/collatinus/ressources/Georges_1913.xml"
		self.sourcelang = "de"
		self.targetlang = "fr"


class Calonghi(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		#Based on Biblissima
		self.url = "http://outils.biblissima.fr/collatinus/ressources/Calonghi_1898.djvu"
		self.sourcelang = "de"
		self.targetlang = "it"

