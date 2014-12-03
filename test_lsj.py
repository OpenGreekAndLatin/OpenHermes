#!/usr/bin/python
# -*- coding: utf-8 -*-

from Corpus import greek

GreekDic = {
	"LSJ" : greek.LSJ()
}

GreekDic["LSJ"].convert()