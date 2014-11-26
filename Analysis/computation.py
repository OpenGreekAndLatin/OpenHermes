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

	def similarity(self):
		pos = 'ADJ'
		for lang in self.freqdist.keys():
			print(lang)
			self.normal_df(self.freqdist[lang][pos])
			self.scores[lang][pos] = pandas.DataFrame(
				p_d(self.df, metric=self.metric),
				index=self.df.index,
				columns=self.df.index)
		#scores = defaultdict(dict)
		#count = 0
		#for w1, w2 in combinations(self.freqdist.keys(), 2):
		#	if count % 100000 == 0:
		#		print('%s combo at %s' % (count,
		#								  datetime.datetime.now().isoformat()))
		#	score = p_d(pandas.DataFrame([self.freqdist[w1],
		#								  self.freqdist[w2]]).fillna(0),
		#				metric=self.metric)
		#	scores[w1][w2] = scores[w2][w1] = score
		#	count += 1
		#return dict(scores)

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
						for i, sense in enumerate(senses):
							sense = re.sub(pattern, ' ', sense).lower()
							f_d['-'.join([key, str(i)])] = Counter(sense.split())
					else:
						try:
							sense = re.sub(pattern, ' ', senses[0]).lower()
							f_d[key] = Counter(sense.split())
						except IndexError as E:
							f_d[key] = {}
				self.freqdist[lang][pos] = f_d

	def normal_df(self, d):
		self.df = pandas.DataFrame(d).fillna(0).T

	def sparsify(self):
		self.df = pandas.SparseDataFrame(self.freqdist)
		#return self.sparse_df
