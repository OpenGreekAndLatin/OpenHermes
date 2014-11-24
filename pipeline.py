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

for lang in CollatinusDic:
	CollatinusDic[lang].convert()