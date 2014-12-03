#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys

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
		"it" : Collatinus("la"),
		"pt" : Collatinus("pt")
	}, "(Latin) Corpus based on Collatinus lexicons"]
]

AvailableAlgorythm = [
	["CosineSim", computation.CosineSim, "A Cosine similarity algorythm"]
]

if __name__ == "__main__":

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:",["corpus=", "help", "algorythm="])
	except getopt.GetoptError:
		opts = []

	corpus = None
	algorythm = AvailableAlgorythm[0][1]
	algorythmString = AvailableAlgorythm[0][0]

	for o in opts:
		if o[0] in ["h", "--help"]:
			print( """{0}Help for Open Philology Synonym Generator{1}

{3}Commands:{1}
{2}--corpus= , c{1}\t Define the corpus
{2}--algorythm= , a{1}\t Define the algorythm you're using""".format(color.DARKCYAN, color.END, color.BLUE, color.UNDERLINE))

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
		if o[0] in ["c", "--corpus"]:
			if o[1].isdigit():
				z = int(o[1])
				if len(AvailableCorpus) - 1 > z:
					corpus = AvailableCorpus[z]
			else:
				match = [group for group in AvailableCorpus if group[0] == o[1]]
				if len(match) == 1:
					corpus = match[0]
		if o[0] in ["a", "--algorythm="]:
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

if corpus == None:
	print("Unknown Corpus")
	sys.exit()



corpusObj = corpus[1]
data = {}
for lang in corpusObj:
	data[lang] = corpusObj[lang].convert()

inst = algorythm(data)
inst.dictConvert()

for dic in inst.data:
	for key in inst.data[dic]:
		print(key)
inst.similarity()
for POS in inst.average:
	inst.average[POS].to_csv("Results/OGL_{0}_{1}_{2}_average.csv".format(POS, algorythmString, corpus[0]))
	print ("Results saved to Results/OGL_{0}_{1}_{2}_average.csv".format(POS, algorythmString, corpus[0]))