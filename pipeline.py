#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file contains the whole algorithm

from Corpus import dictionaries
from Corpus import latin

Dictionaries = {
	"Calonghi" : latin.Calonghi(),
	"Gaffiot" : latin.Gaffiot(),
	"LS" : latin.LS(),
	"Georges" : latin.Georges(),
}

#Install part
for dictionaryName in Dictionaries:
	Dictionaries[dictionaryName].install()