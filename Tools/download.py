#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wget
import subprocess
import shutil


class File(object):
	def __init__(self, url, path, filename, mime = None):
		"""
		Download a file at @url and put it in Software_Root/path/filename
		"""
		self.__dir__ = os.path.dirname(os.path.abspath(__file__))
		self.path = os.path.join(self.__dir__, "../{0}/{1}".format(path, filename))
		self.path = os.path.abspath(self.path)

		self.filename = filename
		self.url = url
		self.mime = mime

	def download(self):
		try:
			filename = wget.download(self.url, self.path)
			#os.rename(os.path.join(self.__dir__, filename), self.path)
			return True
		except Exception as E:
			print(E)
			return False

	def check(self, force = False):
		if os.path.isfile(self.path) == False:
			if force == True:
				return self.download()
			else:
				return False
		return True


class Copyrighted(File):
	def __init__(self, destination, filename, origin = ""):
		self.__dir__ = os.path.dirname(os.path.abspath(__file__))
		self.path = os.path.join(self.__dir__, "../{0}/{1}".format(destination, filename))
		self.path = os.path.abspath(self.path)
		self.filename = filename

		self.origin = os.path.abspath(os.path.join(self.__dir__, "../Copyrighted/{0}{1}".format(origin, filename)))

	def download(self):
		try :
			shutil.copyfile(self.origin, self.path)
			return True
		except Exception as E:
			print(E)
			return False
		

class Github(object):
	def __init__(self, user, repository, path):
		"""
			Clone a @user/@repository in given /Software_Root/path
		"""
		self.__dir__ = os.path.dirname(os.path.abspath(__file__))
		self.path = os.path.join(self.__dir__, "../{0}".format(path))
		self.repository = repository
		self.user = user

	def url(self):
		return "https://github.com/{0}/{1}.git".format(self.user, self.repository)

	def check(self):
		return os.path.isdir(self.path)

	def clone(self):
		return subprocess.call(['git', 'clone', self.url(), self.path])
