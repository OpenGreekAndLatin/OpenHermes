#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file contains the whole algorithm

from Corpus import dictionaries
Dictionaries = {
	"Calonghi" : dictionaries.Calonghi(),
	"Gaffiot" : dictionaries.Gaffiot(),
	"LS" : dictionaries.LS(),
	"Georges" : dictionaries.Georges(),
}

#Install part
for dictionaryName in Dictionaries:
	Dictionaries[dictionaryName].install()