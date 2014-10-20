#!/usr/bin/python
# -*- coding: utf-8 -*-

class A(object):
	def __init__(self):
		self.text = "Hello"

class B(object):
	def __init__(self):
		self.A = A()

b = B()
print b.A.text
print getattr(b, "A")


def subAttr( attributeString, instance):
	o = instance
	i = 0
	attributeList = attributeString.split(".")
	print attributeList
	for attr in attributeList:
		if hasattr(o, attr):
			o = getattr(o, attr)
		else:
			raise ValueError("This object has no attribute {0}".format(attributeString))
		i += 1
		if i == len(attributeList):
			return o

print subAttr("A.text", b)