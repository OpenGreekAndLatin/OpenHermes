#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file contains the whole algorithm

from Corpus import dictionaries
from Corpus import latin
from Corpus import greek

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
"""
for dictionaryName in Dictionaries:
	Dictionaries[dictionaryName].install()
"""

LSJ = greek.LSJ()
print LSJ.install()