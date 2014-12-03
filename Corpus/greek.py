#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys
sys.path.append("../")

from Corpus.dictionaries import Dictionary
from Tools.download import GithubDir

import xml.etree.cElementTree as cElementTree
from collections import defaultdict
import glob
import re

class LSJ(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		#Based on Perseus Digital Library
		#self.url = "https://github.com/PerseusDL/lexica/tree/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/*.xml"
		self.sourcelang = "gr"
		self.targetlang = "en"
		self.file =  GithubDir("PerseusDL", "lexica", "Files/LSJ", sourceDir = "CTS_XML_TEI/perseus/pdllex/grc/lsj")

		self.getPath(self.__class__.__name__)

	def install(self):
		return self.download()

	def download(self):
		return self.file.download()

	def TEIConverter(self, POS):
		"""
			Common method for LS and LSJ as they share the same structure
		"""
		#I think we should move from BS to something else...
		files = glob.glob('/'.join([self.file.path, '*.xml']))
		data = {}

		space_remover = re.compile("([\s]+)")

		for pos in POS:
			data[POS[pos]] = defaultdict(list)

		pos = None

		for file in files:
			tree = cElementTree.parse(file)
			root = tree.getroot()
			for word in root.findall('.//entryFree'):
				pos = word.find("./pos[@TEIform='pos']")
				if cElementTree.iselement(pos):
					pos_text = space_remover.sub("", pos.text)
					if pos_text in POS:
						pos = POS[pos_text]
						orth = word.find("./orth").text
						senses = word.findall('./sense/tr')
						text = " ".join([s.text for s in senses])
						data[pos][orth].append(text)
		self.data = data
		return data

	def callback(self):
		return self.TEIConverter(
			POS = {
				"Adj." : "ADJ",
				"Subst." : "N"
			}
		)

	def convert(self, force = False):
		return self._convert(force, callback = self.callback)