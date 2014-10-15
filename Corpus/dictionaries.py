#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys

sys.path.append("../")

import os
from Tools.download import File
from Tools.download import Copyrighted

from bs4 import BeautifulSoup as b_soup
from collections import defaultdict

class Dictionary(object):
	def __init__(self):
		self.sourcelang = None
		self.targetlang = None
		self.url = None

	def install(self):
		raise NotImplementedError("Install is not installed")

	def toDataformat(self, data):
		"""
			Should convert to Pickle right now, keeping toDataformat broad...
		"""
		raise NotImplementedError("toDataformat is not implemented")

	def checkConverted(self):
		raise NotImplementedError("CheckConverted is not implemented")

	def convert(self, force = True):
		"""
			Force parameters should force creating, while normal behaviour should use checkConverted
			Then it should call self.toPickle
		"""
		raise NotImplementedError("Convert is not implemented")

	def search(self):
		raise NotImplementedError("Install is not installed")

	def download(self):
		filename = os.path.basename(self.url)
		self.download = File(self.url, "Files", filename)
		return self.download.check(force=True)



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
