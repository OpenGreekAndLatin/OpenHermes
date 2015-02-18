#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/")

# Process
from Analysis.process import OpenSynonyms
# Analysis
from Analysis import computation
# Shelves
from Corpus.collatinus import Collatini
from Corpus.greek import Greek
# Commandlines
from Tools.cmd import color


# We set up a list of available to run corpus
# Tuples
AvailableCorpus = [
    ["Greek", Greek, "(Greek) Corpus based on LSJ"],
    ["Collatinus", Collatini, "(Latin) Corpus based on Collatinus lexicons"]
]

AvailableAlgorythm = [
    ["CosineSim", computation.CosineSim, "A Cosine similarity algorythm using normal frequencies"],
    ["TfIDFCosineSim", computation.TfIdfCosineSim, "A Cosine similarity algorythm using Tf-Idf weighted frequencies"]
]

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["corpus=", "help", "algorythm=", "force=", "csv", "csv=", "search="])
    except getopt.GetoptError:
        opts = []

    corpus = None
    algorythm = AvailableAlgorythm[0][1]
    algorythmString = AvailableAlgorythm[0][0]
    force = False
    export = None
    search = None

    for o in opts:
        if o[0] in ["h", "--help"]:
            print("""{0}Help for Open Philology Synonym Generator{1}

{3}Commands:{1}
{2}--corpus= , c{1}\t Define the corpus
{2}--algorythm= , a{1}\t Define the algorythm you're using
{2}--search=POS,{1}\t Search for synonyms given. Parameter is using format PartOfSpeach,lemma
{2}--csv,--csv=path {1}\t Export results to csv. If --csv=path, then exporting to given path
{2}--force=0{1}\t Force the reconstruction of the cache. --force=1 means you reconstruct. Default 0""".format(color.DARKCYAN, color.END, color.BLUE, color.UNDERLINE))

            print ("\n{0}Corpora:{1}".format(color.UNDERLINE, color.END))
            i = 0
            for corpus in AvailableCorpus:
                print ("{0}\t {1} \t\te.g. {4}--corpus={2}, -c{3}, -c{2}{5}".format(color.BLUE + corpus[0] + color.END, corpus[2], corpus[0], i, color.DARKCYAN, color.END))
                i += 1

            print ("\n{0}Algorythms:{1}".format(color.UNDERLINE, color.END))
            i = 0
            for algo in AvailableAlgorythm:
                print ("{0}\t {1} \t\te.g. {4}--algorythm={2}, -a {3}, -a {2}{5}".format(color.BLUE + algo[0] + color.END, algo[2], algo[0], i, color.DARKCYAN, color.END))
                i += 1
            sys.exit()
        if o[0] in ["--force"]:
            if o[1].isdigit():
                z = int(o[1])
                if z == 1:
                    force = True
        if o[0] in ["c", "--corpus"]:
            if o[1].isdigit():
                z = int(o[1])
                if len(AvailableCorpus) - 1 > z:
                    corpus = AvailableCorpus[z]
            else:
                match = [group for group in AvailableCorpus if group[0] == o[1]]
                if len(match) == 1:
                    corpus = match[0]
        if o[0] in ["a", "--algorythm"]:
            if o[1].isdigit():
                z = int(o[1])
                if len(AvailableAlgorythm) - 1 > z:
                    algorythm = AvailableAlgorythm[z][1]
                    algorythmString = AvailableAlgorythm[z][0]
            else:
                match = [group for group in AvailableAlgorythm if group[0] == o[1]]
                if len(match) == 1:
                    algorythm = match[0][1]
                else:
                    print("Unknown algorythm")
                    sys.exit()

        if o[0] in ["--csv"]:
            export = "csv"
            path = None
            if len(o[1]) > 0:
                path = o[1]

        if o[0] in ["--search"]:
            r = o[1].split(",")
            search = (r[0], "".join(r[1:]))

    if corpus is None:
        print("Unknown Corpus")
        sys.exit()

    instance = OpenSynonyms(
        corpus=corpus[1],
        algorythm=algorythm
    )
    instance.generate()
    instance.analyse(debug=True)

    if type(search) == tuple:
        try:
            results = instance.search(
                POS=search[0],
                lemma=search[1]
            )
        except Exception as E:
            print (E)
            sys.exit()

        print ("{1}Score{0}\t\t\t{2}Lemma{0}".format(color.END, color.DARKCYAN, color.BLUE))
        print ("{1}----------------------{0}".format(color.END, color.RED))
        for result in results:
            print ("{1}{3}{0}\t{2}{4}{0}".format(color.END, color.DARKCYAN, color.BLUE, result[1], result[0]))

    if export == "csv":
        instance.to_csv(debug=True)
