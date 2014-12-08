#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import os
import pickle


class OpenSynonyms(object):
	def __init__(self, corpus, algorythm, name = "OpenSynonyms"):
		self.corpus = corpus
		self.algorythm = algorythm
		self.path = os.path.dirname(os.path.abspath(__file__))

		self.name = name

	def search(self, POS = "N", lemma = "bonus"):
		if not self.results:
			self.analyse()
		if POS not in self.results:
			raise ValueError("This PartOfSpeach is not available in this Corpus")

		found = self.results[POS]
		found = found.sort(lemma, ascending=True)
		found = found[lemma]
		found = found[found > 0.0]
		found_subset = found[1:10]
		heads = found_subset.keys().tolist()
		found_subset = found_subset.tolist()

		return list(zip(heads, found_subset))

	def checkCacheAnalyse(self):
		return False

	def generate(self, force = False):
		""" Read and Generate the dictionaries """
		data = {}
		for lang in self.corpus:
			data[lang] = self.corpus[lang].convert(force = force)
		self.data = data
		return data

	def analyse(self, force = False, debug = False, path = None):
		if self.from_pickle(path):
			return self.results

		""" Run the algorythm on the corpus """
		self.instance = self.algorythm(self.data)
		self.instance.dictConvert()
		self.instance.similarity()

		self.results = self.instance.average

		self.to_pickle(debug = debug, path = path)
		return self.results 

	def from_pickle(self, path = None, debug = False):
		if not path:
			path = self.path + "/Cache/"
		path = "{0}OGL_{1}_{2}_average.pickle".format(path, self.algorythm.__name__, self.name)

		if not os.path.isfile(path):
			return False
			
		with open(path, "rb") as f:
			self.results = pickle.load(f)
			return self.results
		return False

	def to_pickle(self, path = None, debug = False):
		if not path:
			path = self.path + "/Cache/"
		path = "{0}OGL_{1}_{2}_average.pickle".format(path, self.algorythm.__name__, self.name)

		with open(path, "wb") as f:
			pickle.dump(self.results, f)

		if debug == True:
			print ("Results saved to {0}".format(path))


	def to_csv(self, path = None, debug = False):
		for POS in self.results:
			if not path:
				path = self.path + "/Results/"

			path = "{0}OGL_{1}_{2}_{3}_average.csv".format(path, POS, self.algorythm.__name__, self.name)

			self.results[POS].to_csv(path)
			if debug == True:
				print ("Results saved to {0}".format(path))

#############################################################################################
#
#
#	Commandline part
#
#
#############################################################################################

from Corpus import latin, greek
from Corpus.collatinus import Collatinus
from Analysis import computation

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#We set up a list of available to run corpus
#Tuples
AvailableCorpus = [
	["Greek", {
		"LSJ" : greek.LSJ()
	}, "(Greek) Corpus based on LSJ"],
	["Collatinus", {
		"en" : Collatinus("uk"),
		"fr" : Collatinus("fr"),
		"de" : Collatinus("de"),
		"ca" : Collatinus("ca"),
		"gl" : Collatinus("gl"),
		"it" : Collatinus("it"),
		"pt" : Collatinus("pt")
	}, "(Latin) Corpus based on Collatinus lexicons"]
]

AvailableAlgorythm = [
	["CosineSim", computation.CosineSim, "A Cosine similarity algorythm using normal frequencies"],
	["TfIDFCosineSim", computation.TfIdf, "A Cosine similarity algorythm using Tf-Idf weighted frequencies"]
]

if __name__ == "__main__":

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:",["corpus=", "help", "algorythm=", "force=", "csv", "csv=", "search="])
	except getopt.GetoptError:
		opts = []

	corpus = None
	algorythm = AvailableAlgorythm[0][1]
	algorythmString = AvailableAlgorythm[0][0]
	force = False
	export = None
	search = None

	for o in opts:
		if o[0] in ["h", "--help"]:
			print( """{0}Help for Open Philology Synonym Generator{1}

{3}Commands:{1}
{2}--corpus= , c{1}\t Define the corpus
{2}--algorythm= , a{1}\t Define the algorythm you're using
{2}--search=POS,{1}\t Search for synonyms given. Parameter is using format PartOfSpeach,lemma
{2}--csv,--csv=path {1}\t Export results to csv. If --csv=path, then exporting to given path
{2}--force=0{1}\t Force the reconstruction of the cache. --force=1 means you reconstruct. Default 0""".format(color.DARKCYAN, color.END, color.BLUE, color.UNDERLINE))

			print ("\n{0}Corpora:{1}".format(color.UNDERLINE, color.END))
			i = 0
			for corpus in AvailableCorpus:
				print ("{0}\t {1} \t\te.g. {4}--corpus={2}, -c{3}, -c{2}{5}".format(color.BLUE + corpus[0] + color.END, corpus[2], corpus[0], i, color.DARKCYAN, color.END))
				i += 1

			print ("\n{0}Algorythms:{1}".format(color.UNDERLINE, color.END))
			i = 0
			for algo in AvailableAlgorythm:
				print ("{0}\t {1} \t\te.g. {4}--algorythm={2}, -a {3}, -a {2}{5}".format(color.BLUE + algo[0] + color.END, algo[2], algo[0], i, color.DARKCYAN, color.END))
				i += 1
			sys.exit()
		if o[0] in ["--force"]:
			if o[1].isdigit():
				z = int(o[1])
				if z == 1:
					force = True
		if o[0] in ["c", "--corpus"]:
			if o[1].isdigit():
				z = int(o[1])
				if len(AvailableCorpus) - 1 > z:
					corpus = AvailableCorpus[z]
			else:
				match = [group for group in AvailableCorpus if group[0] == o[1]]
				if len(match) == 1:
					corpus = match[0]
		if o[0] in ["a", "--algorythm"]:
			if o[1].isdigit():
				z = int(o[1])
				if len(AvailableAlgorythm) - 1 > z:
					algorythm = AvailableAlgorythm[z][1]
					algorythmString = AvailableAlgorythm[z][0]
			else:
				match = [group for group in AvailableAlgorythm if group[0] == o[1]]
				if len(match) == 1:
					algorythm = match[0]
				else:
					print("Unknown algorythm")
					sys.exit()

		if o[0] in ["--csv"]:
			export = "csv"
			path = None
			if len(o[1]) > 0:
				path = o[1]

		if o[0] in ["--search"]:
			r = o[1].split(",")
			search = (r[0], "".join(r[1:]))

	if corpus == None:
		print("Unknown Corpus")
		sys.exit()

	instance = OpenSynonyms(
			corpus = corpus[1],
			algorythm = algorythm,
			name = corpus[0]
		)
	instance.generate()
	instance.analyse(debug = True)

	if type(search) == tuple:
		results = instance.search(POS = search[0], lemma = search[1])
		print ("{1}Score{0}\t\t\t{2}Lemma{0}".format(color.END, color.DARKCYAN, color.BLUE))
		print ("{1}----------------------{0}".format(color.END, color.RED))
		for result in results:
			print ("{1}{3}{0}\t{2}{4}{0}".format(color.END, color.DARKCYAN, color.BLUE, result[1], result[0]))

	if export == "csv":
		instance.to_csv(debug = True)