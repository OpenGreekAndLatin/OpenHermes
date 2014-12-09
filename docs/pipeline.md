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
When creating a new `Shelf` object, the object should have a `data` properties containing 

#Computation object

##Import
`from Analysis.computation import Computation`

##Required data

##Required functions
- `Computation.dictConvert(self,data)` transforms and cache `Shelf.data` for further reuse in `similarity`.
- `Computation.similarity(self)` computes 