#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file contains the whole algorithm

from Corpus import latin, greek
from Corpus.collatinus import Collatinus

"""
LatinDic = {
	"Calonghi" : latin.Calonghi(),
	"Gaffiot" : latin.Gaffiot(),
	"LS" : latin.LS(),
	"Georges" : latin.Georges(),
}

GreekDic = {
	"LSJ" : greek.LSJ()
}

#Install part
for dictionaryName in LatinDic:
	LatinDic[dictionaryName].install()

for dictionaryName in GreekDic:
	GreekDic[dictionaryName].install()
	
LatinDic["LS"].install()
print (LatinDic["LS"].convert())
"""

CollatinusDic = {
	"en" : Collatinus("uk"),
	"fr" : Collatinus("fr"),
	"de" : Collatinus("de"),
	"ca" : Collatinus("ca"),
	"gl" : Collatinus("gl"),
	"it" : Collatinus("la"),
	"pt" : Collatinus("pt")
}

data = {}

for lang in CollatinusDic:
	data[lang] = CollatinusDic[lang].convert()

for lang in data:
	for POS in data[lang]:
		count = 0
		for translation in data[lang][POS]:
			count += len(data[lang][POS][translation])
		print( "POS {0} in language {1} has {2} records with {3} translations".format(POS, lang, len(data[lang][POS]), count))
