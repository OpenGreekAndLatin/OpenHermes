#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
sys.path.append("../")

from nose import with_setup

from Analysis.computation import TfIdfCosineSim
from Corpus.collatinus import Collatinus


Col = Collatinus("uk")
source_data = {
	"fr" : {
		"N" : {
			"absida": "1 - l'arc, voûte. - 2 - la course d'une planète. - 3 - le choeur (d'une église), l'abside.",
			"tempus" : "1. le moment, l'instant, le temps 2. l'occasion 3. la circonstance, la situation",
			"aetas" : "1. le temps de la vie, la vie 2. l'âge 3. la jeunesse 4. te temps, l'époque (in aetatem : pendant longtemps)"
		}
	},
	"en" : {
		"N" : {
			"absida" : "apse, apsis; (arched/domed part of building, at end of choir/nave of church);",
			"tempus" : "time, condition, right time; season, occasion; necessity;",
			"aetas" : "lifetime, age, generation; period; stage, period of life, time, era;"
		}
	},
	"it" : {
		"N" : {
			"absida" : "1 - l'arco, volta. - 2 - la corsa di un pianeta. - 3 - il coro, di una chiesa, l'abside.",
			"tempus" : "1. il momento, l'istante, il tempo,2. l'opportunità3. la circostanza, la situazione,",
			"aetas" : "1. il tempo della vita, la vita,2. l'età3. la gioventù4. tu tempo, l'epoca, in aetatem,: per molto tempo,"
		}
	}
}
test_data = {}
for lang, pos_dic in source_data.items():
	test_data[lang] = {}

	for pos, lemma_dict in pos_dic.items():
		test_data[lang][pos] = {}

		for lemma, senses in lemma_dict.items():
			test_data[lang][pos][lemma] = Col.senseSplitter.split(senses)

def test_tf_idf():
	Analyser = TfIdfCosineSim(test_data)
	Analyser.dictConvert()

	#Verifying one frequency counter : italian noun tempus has "la" twice
	assert Analyser.freqdist["it"]["N"]["tempus"]["la"] == 2

	Analyser.similarity(POS = ["N"])

	assert Analyser.average["N"]["tempus"]["tempus"] <= 0