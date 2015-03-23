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
* The functionality here (in test.py) requires access to our document collection, but can be modified for your dataset without much editing. 
* For the dataset column, u = url, t = title, c = content

| Algorithm |  Dataset  | Lvl | Correct | Incorr. | Unknown | Prec.  | Recall |
|-----------|-----------|-----|---------|---------|---------|--------|--------|
| LICA      | u         | 1+2 | 251,470 | 139,102 | 609,429 | 64.385 | 39.057 |
| LICA      | u         | 1   | 327,705 | 62,867  | 609,429 | **83.904** | 39.057 |
| LICA      | u + t     | 1+2 | 252,381 | 158,486 | 589,134 | 61.426 | 41.087 |
| LICA      | u + t     | 1   | 334,904 | 75,963  | 589,134 | 81.512 | 41.087 |
| LICA      | u + t + c | 1+2 | 150,743 | 260,887 | 588,371 | 36.621 | 41.163 |
| DFR (all) | u         | 1+2 | 373,158 | 401,885 | 224,958 | 48.147 | 77.504 |
| DFR (all) | u         | 1   | 397,866 | 377,177 | 224,958 | 51.335 | 77.504 |
| DFR (all) | u + t     | 1+2 | 467,160 | 354,201 | 178,640 | 56.876 | 82.136 |
| DFR (all) | u + t     | 1   | 488,060 | 333,301 | 178,640 | 59.421 | 82.136 |
| DFR (all) | u + t + c | 1+2 | 538,026 | 333,899 | 128,076 | 61.706 | 87.192 |
| DFR rules | u         | 1+2 | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules | u         | 1   | 373,773 | 387,174 | 239,054 | 49.119 | 76.095 |
| DFR rules | u + t     | 1+2 | 337,687 | 423,260 | 239,054 | 44.377 | 76.095 |
| DFR rules | u + t     | 1   | 373,773 | 387,174 | 239,054 | 49.119 | 76.095 |
