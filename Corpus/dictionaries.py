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