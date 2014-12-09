Pipeline of OpenSynonyms
=======================

#Description of the Pipeline
This project is built around different classes: `Computation`, `Dictionary`, `Shelf`. Those classes are then used for `OpenSynonyms` process

#Dictionary object

##Import
`from Corpus.dictionaries import Dictionary`

#Shelf object

##Import
`from Corpus.dictionaries import Shelf`

##Implementation
When creating a new `Shelf` object, the object should have a `data` properties containing a dictionary where keys are string and values are `Dictionary` instances.

#Computation object

##Import
`from Analysis.computation import Computation`

##Required data
- `Computation.scores`
- `Computation.average`
- `Computation.freqdist`

##Required functions
- `Computation.dictConvert(self,data)` transforms and cache `Shelf.data` for further reuse in `similarity`.
- `Computation.similarity(self, POS = ["N", "ADJ", "V"] debug = True)` computes and returns a `Computation.average` object where depth *n*'s key is a `POS` and its `value` a DataFrame