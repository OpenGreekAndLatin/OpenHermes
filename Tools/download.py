#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import wget
import subprocess
import shutil
import zipfile

class File(object):
	def __init__(self, url, path, filename, mime = None):
		"""
		Download a file at @url and put it in Software_Root/path/filename
		"""
		dir = os.path.dirname(os.path.abspath(__file__))
		self.dir = os.path.abspath(os.path.join(dir, "../{0}".format(path)))
		self.path = os.path.join(dir, "../{0}/{1}".format(path, filename))
		self.path = os.path.abspath(self.path)

		self.filename = filename
		self.url = url
		self.mime = mime

	def directory(self, dir = None):
		if not dir:
			dir = self.dir

		if not os.path.exists(dir):
			return os.makedirs(dir)
		return False

	def download(self):
		self.directory()
		try:
			filename = wget.download(self.url, self.path)
			return True
		except Exception as E:
			print E
			return False

	def check(self, force = False):
		if os.path.isfile(self.path) == False:
			if force == True:
				return self.download()
			else:
				return False
		return True

	def unzip(self, path = None, sourceDir = None):
		if not path:
			path = self.path
		self.directory(path)
		with zipfile.ZipFile(self.path, 'r') as myzip:
			filelist = myzip.namelist()
			if sourceDir:
				filelist = [f for f in filelist if f.startswith(sourceDir) and not f.endswith("/")]
			if len(filelist) == 0:
				raise ValueError("The filelist is empty, nothing to unzip")
			for filepath in filelist:
				try:
					filename = os.path.basename(filepath)
					source = myzip.open(filepath)
					target = file(os.path.join(path, filename), "wb")
					with source, target:
						shutil.copyfileobj(source, target)
				except Exception as E:
					print E
					return False
			return True
		return False



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
			print E
			return False
		

class Github(object):
	def __init__(self, user, repository, path):
		"""
			Clone a @user/@repository in given /Software_Root/path
		"""
		self.__dir__ = os.path.dirname(os.path.abspath(__file__))
		self.path = os.path.abspath(os.path.join(self.__dir__, "../{0}".format(path)))
		self.repository = repository
		self.user = user
		self.file = None

	def url(self):
		return "https://github.com/{0}/{1}.git".format(self.user, self.repository)

	def check(self):
		return os.path.isdir(self.path)

	def clone(self):
		return subprocess.call(['git', 'clone', self.url(), self.path])

	def zip(self):
		self.file = File(
				url = "https://github.com/{0}/{1}/archive/master.zip".format(self.user, self.repository), 
				path = "Files/Zip", 
				filename = self.repository + ".zip"
			)
		if not self.file.check():
			return self.file.download()
		return True

class GithubDir(Github):
	def __init__(self, user, repository, path, sourceDir, branch = "master"):
		super(self.__class__, self).__init__(user, repository, path)
		self.branch = branch
		self.sourceDir = sourceDir
		self.sourceDir = "{0}-{1}/{2}".format(self.repository, self.branch, self.sourceDir)

	def download(self):
		#First step, with get the dir
		if self.zip():
			return self.file.unzip(path = self.path, sourceDir = self.sourceDir )
		return False