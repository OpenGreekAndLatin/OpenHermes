Open_Philology_Synonyms
=======================

This is the work on automatic creation of thesauri

##Download Module
**Required Module** : wget

##Corps.dictionaries
Hold the dictionary entities to download them and convert them to data for the DataModel

##Stop words, you said stopwords ?
Because we are dealing with small data for some lexicons or dictionaries, we need to ensure there is not too much noise. For this reason, we use few stopwords, found mainly on [discoverysearchengine](http://www.discoverysearchengine.com/reference/text_dimensions.html).

But we can't use a strong stopwords list : we shouldn't avoid some common name such as "good" as it can be the only translation for one word such as bonus. We use a list of simple stopwords, according to [Text Analytics 101](http://www.text-analytics101.com/2014/10/all-about-stop-words-for-text-mining.html)

> Examples of minimal stop word lists that you can use:
> - **Determiners** - Determiners tend to mark nouns where a determiner usually will be followed by a noun (*examples: the, a, an, another*)
> - **Coordinating** conjunctions – Coordinating conjunctions connect words, phrases, and clauses (*examples: for, an, nor, but, or, yet, so*)
> - **Prepositions** - Prepositions express temporal or spatial relations (*examples: in, under, towards, before*)
