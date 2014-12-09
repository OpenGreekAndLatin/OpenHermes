#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas

from sklearn.metrics.pairwise import pairwise_distances as p_d

from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer

from collections import Counter, defaultdict
import re
from string import punctuation
from itertools import combinations
import datetime

class Computation():

	def __init__(self):
		self.data = None
		self.freqdist = defaultdict(dict)
		self.scores = defaultdict(dict)
		self.globalfreq = defaultdict(dict)

	def similarity(self):
		raise NotImplementedError("similarity is not implemented")

	def checkFormat(self):
		raise NotImplementedError("checkFormat is not implemented")

	def dictConvert(self):
		raise NotImplementedError("dictConvert is not implemented")

	def sparsify(self, dense):
		return dense.to_sparse(fill_value=0)

	def normal_df(self, data):
		self.df = pandas.DataFrame(data).fillna(0).T
		return self.df

	def individualCounterConvert(self):
		""" Implements a counter converts for dictConvert function and sklearn algorythms based on it"""
		freqdist = defaultdict(dict)
		pattern = re.compile(r'[%s]' % (punctuation))
		for lang, val in self.data.items():
			for pos, lemma in val.items():
				f_d = {}
				for key, senses in lemma.items():
					if type(senses) != list:
						raise TypeError('senses has to be a list before Convert()')

					if len(senses) > 1:
						senses = ' '.join(senses)
					else:
						senses = senses[0]

					if type(senses) == list:
						raise TypeError('senses cannot be a list during Convert()')

					try:
						sense = re.sub(pattern, ' ', senses).lower()
						f_d[key] = Counter(sense.split())
					except IndexError as E:
						f_d[key] = {}
				freqdist[lang][pos] = f_d
		return freqdist

	def globalCounterConvert(self):
		""" Turn a Dictionary of [lemma] = { Counter (), Counter ()} to a global CounterDict """
		pattern = re.compile(r'[%s]' % (punctuation))
		for lang, val in self.data.items():
			for pos, lemma in val.items():
				document = []
				for key, senses in lemma.items():
					if type(senses) != list:
						raise TypeError('senses has to be a list before Convert()')

					if len(senses) > 1:
						senses = ' '.join(senses)
					else:
						senses = senses[0]

					if type(senses) == list:
						raise TypeError('senses cannot be a list during Convert()')

					sense = re.sub(pattern, ' ', senses).lower()
					document.append(sense)

				self.globalfreq[lang][pos] = CountVectorizer().fit_transform(document)
		return self.globalfreq

	def posAverage(self, scores):
		""" Scores = scores[pos] """
		average = pandas.concat([scores[lang] for lang in scores])
		average = average.groupby(by = average.index)
		average = average.mean()
		return average


class TfIdfCosineSim(Computation):
	def __init__(self, data):
		self.data = data #Structured as [lang][pos]
		self.freqdist = defaultdict(dict)
		self.metric = 'cosine'
		self.scores = defaultdict(dict)
		self.globalfreq = defaultdict(dict)
		self.average = {}

	def dictConvert(self):
		self.freqdist = self.individualCounterConvert()
		return self.freqdist

	def similarity(self, POS = ['ADJ', 'V', 'N']):
		pos_list = POS
		for pos in pos_list:
			for lang in self.freqdist.keys():
				TfIdf = TfidfTransformer()
				if pos in self.freqdist[lang].keys():
					dataframe = self.normal_df(self.freqdist[lang][pos])

					TfIdf.fit(dataframe)
					data = TfIdf.transform(dataframe)

					self.scores[pos][lang] = pandas.DataFrame(
						p_d(data, metric=self.metric),
						index=dataframe.index,
						columns=dataframe.index)

			self.average[pos] = self.posAverage(self.scores[pos])

		return self.average

class CosineSim(Computation):

	def __init__(self, data):
		self.data = data
		self.metric = 'cosine'
		self.freqdist = defaultdict(dict)
		self.scores = defaultdict(dict)
		self.average = {}

	def similarity(self, POS = ['ADJ', 'V', 'N'], debug = False):
		pos_list = POS
		for pos in pos_list:
			for lang in self.freqdist.keys():
				if pos in self.freqdist[lang].keys():
					if debug:
						print("Computing on {0} / POS {1} ".format(lang, pos))
					self.normal_df(self.freqdist[lang][pos])
					self.scores[pos][lang] = pandas.DataFrame(
						p_d(self.df, metric=self.metric),
						index=self.df.index,
						columns=self.df.index)

			self.average[pos] = self.posAverage(self.scores[pos])

		return self.average

	def checkFormat(self):
		if type(self.data) == pandas.core.frame.DataFrame:
			return self.data
		elif type(self.data) == dict:
			return self.dictConvert()
		else:
			raise TypeError('Data format must be DataFrame or Dictionary')

	def dictConvert(self):
		self.freqdist = self.individualCounterConvert()
		return self.freqdist

	def sparsify(self):
		self.df = pandas.SparseDataFrame(self.freqdist)
		return self.df
