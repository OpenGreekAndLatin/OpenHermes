#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys

sys.path.append("../")

import os
from Tools.download import File
from Tools.download import Copyrighted

import xml.etree.cElementTree as cElementTree
from collections import defaultdict
import glob
import pickle


class Dictionary(object):
	def __init__(self):
		self.sourcelang = None
		self.targetlang = None
		self.url = None
		self.data = {}

	def getPath(self, className):
		self.path = os.path.dirname(os.path.abspath(__file__)) + "/../Cache/{0}-{1}-{2}.pickle".format(className, self.sourcelang, self.targetlang)
		return self.path

	def install(self):
		raise NotImplementedError("Install is not installed")

	def load(self):
		"""
			Should read and import data from pickle
		"""
		if os.path.isfile(self.path):
			with open(self.path, "rb") as f:
				self.data = pickle.load(f)
			return True
		return False

	def dump(self):
		"""
			Should convert to Pickle right now, keeping toDataformat broad...
		"""
		with open(self.path, "wb") as f:
			pickle.dump(self.data, f)
		return True

	def checkConverted(self):
		raise NotImplementedError("CheckConverted is not implemented")

	def convert(self, fn = False, force=True):
		"""
			Force parameters should force creating, while normal behaviour should use checkConverted
			Then it should call self.toPickle
		"""
		raise NotImplementedError("Convert is not implemented")
		if force:
			pass

	def search(self):
		raise NotImplementedError("Install is not installed")

	def download(self):
		filename = os.path.basename(self.url)
		self.download = File(self.url, "Files", filename)
		return self.download.check(force=True)

	def subAttr(self, attributeString, instance):
		o = instance
		i = 0
		attributeList = attributeString.split(".")
		for attr in attributeList:
			if hasattr(o, attr):
				o = getattr(o, attr)
			else:
				raise ValueError("This object has no attribute {0}".format(attributeString))
			i += 1
			if i == len(attributeList):
				return o

	def _convert(self, force = False, callback = None):
		load = self.load()
		if force == True or load == False:
			callback()
			self.dump()
		return self.data


	def PerseusTEIConverter(self, architecture = "tr.text", POS = {}):
		"""
			Common method for LS and LSJ as they share the same structure
		"""
		raise NotImplementedError("Convert is not implemented")
		self.data = data
		return data
