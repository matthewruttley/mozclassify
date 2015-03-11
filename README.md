# About
Algorithms for URL Classification. Will implement LICA, LWCA, DFR etc

# Usage

For LICA:

    >>> import classifier_LICA
    >>> classifier = classifier_LICA.LICA()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    [u'hobbies & interests', u'coins']

For DFR

    >>> import classifier_DFR
    >>> classifier = classifier_DFR.DFR()
    >>> classifier.classify("http://www.coinweek.com/us-coins/the-marvelous-pogue-family-coin-collection-part-2-the-oliver-jung-1833-half-dime/")
    (u'hobbies & interests', u'coins')
	
Options:

* To use the title as well, use a named argument like: `classifier.classify("http://domain.com", title="Interesting Coin Website")`
* To use DFR rules only (i.e. no overall LICA-style matching for unknown domains), add a `rules_only=True` argument

# Performance

* Total documents (i.e. url/title pairs) tested: 1,000,001
* Level refers to returning MozCat level 1 or both 1+2


| Algo      |  Dataset  | Lvl | Correct | Incorr. | Unknown | Prec.  | Recall |
|-----------|-----------|-----|---------|---------|---------|--------|--------|
| LICA      | URLs only | 1+2 | 251,470 | 139,102 | 609,429 | 64.385 | 39.057 |
| LICA      | URLs only | 1   |         |         |         |        |        |
| LICA      | URL+title | 1+2 | 252,381 | 158,486 | 589,134 | 61.426 | 41.087 |
| LICA      | URL+title | 1   |         |         |         |        |        |
| DFR (all) | URLs only | 1+2 | 373,158 | 401,885 | 224,958 | 48.147 | 77.504 |
| DFR (all) | URLs only | 1   |         |         |         |        |        |
| DFR (all) | URL+title | 1+2 | 467,160 | 354,201 | 178,640 | 56.876 | 82.136 |
| DFR (all) | URL+title | 1   |         |         |         |        |        |
| DFR rules | URLs only | 1+2 | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules | URLs only | 1   |         |         |         |        |        |
| DFR rules | URL+title | 1+2 | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules | URL+title | 1   |         |         |         |        |        |
