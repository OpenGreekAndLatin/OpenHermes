#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


from nose import with_setup
from Corpus.collatinus import Collatinus

def test_stopwords_print():
	eng = Collatinus("uk")
	eng.loadStopwords()

	assert "its" in eng.stopwords

def test_remove_stopwords():
	eng = Collatinus("uk")
	eng.loadStopwords()
	clean = eng.removeStopwords("Its support is really important")
	assert clean == "support is really important"

def test_remove_stopwords_on_entry():
	eng = Collatinus("fr")
	eng.convert(force = True)
	#le temps de la vie, la vie 2. l'âge 3. la jeunesse 4. te temps, l'époque (in aetatem : pendant longtemps)
	assert " ".join(eng.data["N"]["aetas"]) == "temps vie vie âge jeunesse temps époque in aetatem pendant longtemps"