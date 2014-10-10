#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import sys for relative import
import sys
sys.path.append("../")

from Tools.download import File

class Dictionary(object):
	def __init__(self):
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