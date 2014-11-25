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
		self.freqdist = {}

	def similarity(self):
		scores = p_d(self.sparse_df, metric=self.metric)
		return pandas.DataFrame(scores,
                                        index=self.sparse_df.index,
                                        columns=self.sparse_df.index)
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
		for key, senses in self.data.items():
			if len(senses) > 1:
				for i, sense in enumerate(senses):
					sense = re.sub(pattern, '', sense).lower()
					self.freqdist['-'.join([key, str(i)])] = Counter(sense.split())
			else:
				try:
					sense = re.sub(pattern, '', senses[0]).lower()
					self.freqdist[key] = Counter(sense.split())
				except IndexError as E:
					self.freqdist[key] = {}
		#return pandas.DataFrame(freqdist)
		#return self.freqdist

	def sparsify(self):
		self.sparse_df = pandas.SparseDataFrame(self.freqdist)
		#return self.sparse_df
