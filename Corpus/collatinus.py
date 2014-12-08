#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys
sys.path.append("../")
import os
import re
import unicodedata
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

from Corpus.dictionaries import Dictionary

class Collatinus(Dictionary):
	def __init__(self, lang, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		self.sourcelang = "la"
		self.targetlang = lang
		self.root = os.path.dirname((os.path.abspath(__file__))) + "/../Copyrighted/collatinus/"

		self.latin = self.loadLatin()

		self.tokenizer = RegexpTokenizer(r'\w+')

		#According to document mdlrad.la (Model radical) in collatinus.mdlrad
		self.flexio = {
			"0" : "N", #Noun
			"1" : "N",
			"2" : "N",
			"3" : "N",
			"4" : "N",
			"5" : "N",
			"6" : "N",
			"7" : "N",
			"8" : "N",
			"9" : "N",
			"10" : "N", 
			"11" : "ADJ", #Adjectives
			"12" : "ADJ",
			"13" : "ADJ",
			"14" : "ADJ",
			"15" : "ADJ",
			"16" : "ADJ",
			"17" : "V", #Verb
			"18" : "V",
			"19" : "V",
			"20" : "V",
			"21" : "V",
			"22" : "V",
			"23" : "V",
			"24" : "V",
			"25" : "V",
			"26" : "V",
			"27" : "V",
			"28" : "V",
			"29" : "V",
			"30" : "V",
			"31" : "V",
			"32" : "V",
			"33" : "V",
			"34" : "P", #Pron
			"100" : "Greek", #Unknown as it has a greek translation
			"101" : "Greek",
			"102" : "Greek",
			"103" : "Greek",
			"104" : "Greek",
			"105" : "Greek"
		}
		
		self.senseSplitter = re.compile("(?:\:|\;|[0-9]+\.|(?:[\s]*\-)*[0-9]+[\s]*\-)")
		self.getPath(self.__class__.__name__)

	def install(self):
		raise NotImplementedError("Install is not installed")

	def checkConverted(self):
		raise NotImplementedError("CheckConverted is not implemented")

	def normalize(self, string):
		if "=" in string:
			string = string.split("=")[0]
		sn = unicodedata.normalize('NFKD', string)
		return ''.join(x for x in sn if unicodedata.category(x)[0] == 'L')

	def loadLatin(self):
		data = {}

		with open(self.root + "lemmata.la") as f:
			lines = [line for line in f.read().split("\n") if len(line)>0 and not line[0] == "!"]
		
		for line in lines:
			elements = line.split("|")
			lemma = elements[0]
			lemma = self.normalize(lemma)
			data[lemma] = elements[1]

		return data


	def getPOS(self, lemma):
		if lemma in self.latin:
			flexioNumber = self.latin[lemma]
			if flexioNumber in self.flexio:
				return self.flexio[flexioNumber]
		return "Unknown"

	def callback(self, force=False):
		dictionaries = {
			"V" : defaultdict(list),
			"N" : defaultdict(list),
			"ADJ" : defaultdict(list)
		}
		with open(self.root + "lemmata.{0}".format(self.targetlang)) as f:
			lines = [line for line in f.read().split("\n") if len(line)>0 and not line[0] == "!"]
		
			for line in lines:
				elements = line.split("|")
				lemma = self.normalize(elements[0])
				senses = elements[1]
				senses = self.senseSplitter.split(senses)
				POS = self.getPOS(lemma)
				if POS in dictionaries:
					for sense in senses:
						if len(sense) > 0:
							dictionaries[POS][lemma].append(sense)
					
		return dictionaries

	def convert(self, force = False):
		return self._convert(force = force, callback = self.callback)


