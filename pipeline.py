#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file contains the whole algorithm

from Corpus import latin, greek

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
"""
LSJ = greek.LSJ()
print LSJ.install()
"""
LatinDic["LS"].install()
print (LatinDic["LS"].convert())