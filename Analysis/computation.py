#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas
from sklearn.metrics.pairwise import pairwise_distances as p_d
from collections import Counter, defaultdict
import re
from string import punctuation
from itertools import combinations
import datetime

class Computation():

	def __init__(self):
		self.data = None

	def similarity(self):
		raise NotImplementedError("similarity is not implemented")

	def checkFormat(self):
		raise NotImplementedError("checkFormat is not implemented")

	def dictConvert(self):
		raise NotImplementedError("dictConvert is not implemented")

	def sparsify(self, dense):
		return dense.to_sparse(fill_value=0)



class CosineSim(Computation):

	def __init__(self, data):
		self.data = data
		self.metric = 'cosine'
		self.freqdist = defaultdict(dict)
		self.scores = defaultdict(dict)
		self.average = {}

	def similarity(self, POS = ['ADJ', 'V', 'N']):
		pos_list = POS
		for pos in pos_list:
			for lang in self.freqdist.keys():
				if pos in self.freqdist[lang].keys():
					print("Computing on {0} / POS {1} ".format(lang, pos))
					self.normal_df(self.freqdist[lang][pos])
					self.scores[pos][lang] = pandas.DataFrame(
						p_d(self.df, metric=self.metric),
						index=self.df.index,
						columns=self.df.index)

			self.average[pos] = pandas.concat([self.scores[pos][lang] for lang in self.scores[pos]])
			self.average[pos] = self.average[pos].groupby(by = self.average[pos].index)
			self.average[pos] = self.average[pos].mean()

		return self.average

	def checkFormat(self):
		if type(self.data) == pandas.core.frame.DataFrame:
			return self.data
		elif type(self.data) == dict:
			return self.dictConvert()
		else:
			raise TypeError('Data format must be DataFrame or Dictionary')

	def dictConvert(self):
		pattern = re.compile(r'[%s]' % (punctuation))
		for lang, val in self.data.items():
			for pos, lemma in val.items():
				f_d = {}
				for key, senses in lemma.items():
					if len(senses) > 1:
						senses = ' '.join(senses)
					else:
						senses = senses[0]
					if type(senses) == list:
						raise TypeError('senses cannot be a list')
					try:
						sense = re.sub(pattern, ' ', senses).lower()
						f_d[key] = Counter(sense.split())
					except IndexError as E:
						f_d[key] = {}
				self.freqdist[lang][pos] = f_d

	def normal_df(self, d):
		self.df = pandas.DataFrame(d).fillna(0).T
		return self.df

	def sparsify(self):
		self.df = pandas.SparseDataFrame(self.freqdist)
		return self.df
